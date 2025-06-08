import gradio as gr
import requests
import json
from tenacity import retry, stop_after_attempt, wait_fixed

API_URL = "http://localhost:8000"

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def safe_post(endpoint, files):
    return requests.post(endpoint, files=files)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def safe_get(url):
    return requests.get(url)

def process_file(file):
    file_type = file.name.split(".")[-1].lower()
    endpoint = f"{API_URL}/upload"

    with open(file.name, "rb") as f:
        files = {"file": (file.name, f, "application/octet-stream")}
        response = safe_post(endpoint, files=files)

    memory_response = safe_get(f"{API_URL}/memory/view")

    formatted_response = json.dumps(response.json(), indent=2)
    return formatted_response, memory_response.text

gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload Email / PDF / JSON"),
    outputs=[
        gr.Textbox(label="Agent Response (Formatted JSON)"),
        gr.HTML(label="Memory Log (HTML View)")
    ],
    title="Multi-Agent AI Processor",
    description="Upload a file to classify, route, and view agent memory."
).launch()
