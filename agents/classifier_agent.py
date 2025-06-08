from groq import Groq
import os

client = Groq(api_key="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")

def classify_input(text, format_type):
    prompt = f"""Classify the business intent of this {format_type} input.
Return only one of these intents: RFQ, Complaint, Invoice, Regulation, Fraud Risk.
Input:
{text[:1000]}"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": "You are a business intent classifier."},
            {"role": "user", "content": prompt}
        ]
    )
    intent = response.choices[0].message.content.strip()
    return {"intent": intent}
