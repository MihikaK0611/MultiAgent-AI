from fastapi import FastAPI, UploadFile, File
from agents.classifier_agent import classify_input
from utils.file_parser import get_text_from_file
from memory.memory_store import log_to_memory, get_memory
from routers.action_router import route_action
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
templates = Jinja2Templates(directory="templates")
from fastapi import Request

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename

    # Step 1: Extract text from file
    extracted_text, format_type = get_text_from_file(filename, content)

    # Step 2: Classify format and business intent
    classification = classify_input(extracted_text, format_type)

    # Step 3: Log metadata
    log_to_memory({
        "source": filename,
        "format": format_type,
        "intent": classification["intent"],
    })

    # Step 4: Route to appropriate agent (based on format)
    response = route_action(format_type, extracted_text, classification)

    return {
        "format": format_type,
        "intent": classification["intent"],
        "action_triggered": response
    }

@app.get("/memory/json")
def get_memory_json():
    return get_memory()

@app.get("/memory/view", response_class=HTMLResponse)
def view_memory(request: Request):
    return templates.TemplateResponse("memory.html", {"request": request, "memory": get_memory()})

