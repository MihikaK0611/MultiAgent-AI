import json
from memory.memory_store import log_to_memory
from utils.retry import retry

@retry(max_attempts=3)
def process_json(text):
    alerts = []

    try:
        data = json.loads(text)
        required_fields = ["invoice_number", "total_amount", "customer_id"]

        for field in required_fields:
            if field not in data:
                alerts.append(f"Missing field: {field}")

        if "total_amount" in data and not isinstance(data["total_amount"], (float, int)):
            alerts.append("Amount type error")

        log_to_memory({
            "agent": "json_agent",
            "alerts": alerts,
            "status": "triggered" if alerts else "no alerts",
            "summary": f"Processed JSON, found {len(alerts)} alert(s)." if alerts else "JSON schema validated successfully."
        })

        return alerts if alerts else "JSON Validated"

    except Exception as e:
        log_to_memory({
            "agent": "json_agent",
            "alerts": [str(e)],
            "status": "error",
            "summary": "Failed to parse JSON due to error."
        })
        return "POST /alert/invalid_json"
