from groq import Groq
from memory.memory_store import log_to_memory
from utils.retry import retry

client = Groq(api_key="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")

@retry(max_attempts=3)
def process_email(text):
    prompt = f"""Extract sender, urgency (low, medium, high), issue/request, and tone (angry, polite, threatening) from this email:
{text}"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": "You are an email analysis agent."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()

    # Determine action
    if "angry" in result.lower() or "high" in result.lower():
        action = "POST /crm/escalate"
        status = "triggered"
    else:
        action = "Routine → log and close"
        status = "no escalation"

    # Log to memory
    log_to_memory({
        "agent": "email_agent",
        "result": result,
        "alerts": action,
        "status": status,
        "summary": f"Processed email: escalation {status}."
    })

    return action
