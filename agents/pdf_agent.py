import PyPDF2
from memory.memory_store import log_to_memory
import re
from utils.retry import retry

@retry(max_attempts=3)

def process_pdf(text):
    alerts = []
    if "Invoice" in text:
        match = re.search(r"(?:₹|\$|Rs\.?)?\s?(\d{1,3}(?:,\d{3})+|\d+)", text)
        if match:
            amount = int(match.group(1).replace(",", ""))
            if amount > 10000:
                alerts.append("POST /finance/flag_invoice")
    if any(term in text for term in ["GDPR", "FDA"]):
        alerts.append("POST /compliance/flag")

    log_to_memory({
        "agent": "pdf_agent",
        "alerts": alerts if alerts else [],
        "status": "triggered" if alerts else "no alerts",
        "summary": f"Processed PDF, found {len(alerts)} actionable alert(s)."
    })
    return alerts if alerts else "No alerts"
