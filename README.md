
# 🤖 Multi-Format Autonomous AI System

A smart, context-aware AI system that autonomously processes input files in multiple formats (Email, PDF, JSON), detects business intent, and triggers follow-up actions through chained agents. All processing logic is transparently logged and visualized for traceability.

---

## 🚀 Architecture Overview

### 📦 Components

1. **File Classifier**  
   Detects whether the uploaded file is a PDF, JSON, or Email based on extension and content.

2. **Router**  
   Dynamically routes parsed text content to the correct specialized agent:
   - `pdf_agent.py`
   - `json_agent.py`
   - `email_agent.py`

3. **Specialized Agents**
   Each agent processes content independently and logs alerts or status messages to a central memory store.

4. **Shared Memory Store**  
   Stores all agent actions and logs for monitoring. Data is accessible via:
   - `/memory/json` – raw JSON memory log
   - `/memory/view` – user-friendly HTML table

5. **Gradio Interface**  
   Simple UI to upload files and visualize:
   - Triggered actions
   - Current memory state

---

## 🧠 Agent Logic

### 📄 `pdf_agent.py`
- **Purpose:** Extracts and inspects invoice or policy PDFs.
- **Triggers:**
  - Invoice amount > ₹10,000 → `POST /finance/flag_invoice`
  - Keywords: `GDPR`, `FDA` → `POST /compliance/flag`
- **Output:** Appends alerts to memory with agent name and timestamp.

### 🧾 `json_agent.py`
- **Purpose:** Validates JSON webhook or invoice schema.
- **Triggers:**
  - Missing required fields → `POST /alert/missing_field`
  - Type mismatch (e.g., amount not numeric) → `POST /alert/type_error`
- **Output:** Logs detected anomaly (if any) with description.

### 📨 `email_agent.py`
- **Purpose:** Analyzes tone, urgency, and issue from raw email using Groq + LLaMA 4.
- **Triggers:**
  - Tone: `angry` or Urgency: `high` → `POST /crm/escalate`
- **Output:** Logs extracted summary and triggered action.

---

## 🧪 Sample Inputs

Located in the `/samples` directory:

| File                | Format | Description                             | Expected Outcome                          |
|---------------------|--------|-----------------------------------------|--------------------------------------------|
| `sample_invoice.pdf`| PDF    | Invoice over ₹10,000 + "GDPR" mention   | Finance + Compliance alert                 |
| `sample_email.eml`  | Email  | Angry tone and high urgency             | CRM escalation                             |
| `sample_valid.json` | JSON   | Valid schema, correct types             | No alert                                   |
| `sample_invalid.json`| JSON  | Missing field or wrong type             | Alert for schema violation or type error   |

---

## 📊 Sample Outputs

### 🔍 `/memory/json`  
Returns structured list of all agent responses:
```json
[
  {
    "agent": "pdf_agent",
    "alerts": ["POST /finance/flag_invoice"],
    "timestamp": "2025-06-06T13:20:00"
  },
  {
    "agent": "email_agent",
    "result": "Sender: John, Tone: angry, Urgency: high, Issue: refund",
    "timestamp": "2025-06-06T13:22:45"
  }
]
```

### 🌐 `/memory/view`  
Beautifully rendered table showing agent names, outputs, and timestamps.

---

## 🖼️ Agent Flow Diagram

> *(Located at `diagrams/agent_flow_diagram.png`)*

```
[File Upload] → [Classifier] → [Router]
                           ↓
      ┌────────────┬────────────┬────────────┐
      ↓            ↓            ↓
 [PDF Agent]  [JSON Agent]  [Email Agent]
      ↓            ↓            ↓
  [Alerts]     [Validation]   [Groq + LLaMA]
      ↓            ↓            ↓
   [Shared Memory (JSON & HTML)]
```

---

## 🛠️ How to Run Locally

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start FastAPI app**
   ```bash
   uvicorn main:app --reload
   ```

3. **Launch Gradio interface**
   ```bash
   python ui/app.py
   ```

---

## 📁 Folder Structure

```
multi-agent-ai-system/
├── agents/
├── memory/
├── ui/
├── utils/
├── samples/
├── outputs/
├── diagrams/
├── main.py
└── README.md
```

---

## 🧩 Technologies Used

- **FastAPI** – Backend framework
- **Gradio** – User interface for uploads
- **Groq** – LLaMA 4 inference for email analysis
- **PyPDF2** – PDF parsing
- **Tenacity** – Retry mechanism for robustness
- **Jinja2** – Templated memory HTML view

---

## 🙋‍♀️ Author

**Mihika Khemka**
