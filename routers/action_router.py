from agents.email_agent import process_email
from agents.json_agent import process_json
from agents.pdf_agent import process_pdf

def route_action(format_type, text, classification):
    if format_type == "Email":
        return process_email(text)
    elif format_type == "JSON":
        return process_json(text)
    elif format_type == "PDF":
        return process_pdf(text)
    else:
        return "Unknown format"