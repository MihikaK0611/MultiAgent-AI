from io import BytesIO
import PyPDF2
import json

def get_text_from_file(filename, content):
    if filename.endswith(".pdf"):
        file_stream = BytesIO(content)
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip(), "PDF"

    elif filename.endswith(".json"):
        text = content.decode("utf-8")
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, indent=2), "JSON"
        except:
            return text, "JSON"

    elif filename.endswith(".txt") or filename.endswith(".eml"):
        return content.decode("utf-8"), "Email"

    return content.decode("utf-8"), "Unknown"
