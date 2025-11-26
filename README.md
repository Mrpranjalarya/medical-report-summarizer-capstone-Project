# 🧠 AI Medical Summary Assistant

**Medical Report Summarizer & Patient Support System**  
Built with Google Gemini (LLM), Local Models (optional), and a modular multi-agent architecture.

---

## 🚀 Project Overview

This project is an AI-powered medical report assistant. Users can upload **PDFs, images, or plain text medical reports**, and the system:

- Extracts medical values and findings
- Interprets them in patient-friendly language
- Validates safety and clinical responsibility
- Provides non-prescriptive lifestyle recommendations
- Generates optional AI insights via ADK agent

**Disclaimer:** This tool is **educational only** and **does not replace medical advice**.

---
```bash
## 📂 Project Structure

medical-report-summarizer/
├── .venv/ # Python virtual environment
├── agents/ # AI agents: Extractor, Interpreter, Recommender, Safety, ADK
├── app/ # Streamlit UI
├── data/ # Sample reports and datasets
├── docs/ # Documentation & flowcharts
├── memory/ # Session service and memory storage
├── tests/ # Unit tests
└── tools/ # Utility scripts




---

## 🏗 Architecture & Workflow
```yaml
                🏥 Medical Report (PDF / Image / Text)
                                │
                                ▼
                      [ OCR & Preprocessing Tool ]
                                │
                                ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                        🔁 ADK ORCHESTRATOR (Brain)                      │
 │       Decides which agent runs next, manages context, memory, tools     │
 └────────────────────────────────────────────────────────────────────────┘
                                │
 ┌────────────────────────────────────────────────────────────────────────┐
 │                         👁‍🗨 EXTRACTOR AGENT                           │
 │ Role: Sense                                                         │
 │ Tasks: Identify symptoms, diagnoses, findings, lab values, metrics   │
 │ Tools: OCR, NER, Regex Lab Parser, Medical Ontology API              │
 └────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                        Structured Medical Facts
           (E.g., “LDL 165 mg/dL, Diagnosis: Chronic Bronchitis”)
                                │
                                ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                        🧠 INTERPRETER AGENT                             │
 │ Role: Plan                                                            │
 │ Tasks: Convert medical facts into patient-friendly meaning             │
 │ Models: LLM (Gemini / Med-PaLM), SNOMED mapping                        │
 └────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                   Draft Summary + Medical Interpretation
      (E.g., “Your LDL cholesterol is high and indicates risk of heart disease”)
                                │
                                ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                        🛡 SAFETY VALIDATOR AGENT                       │
 │ Role: Guard                                                            │
 │ Tasks:                                                                 │
 │  ❌ Detect hallucinations                                             │
 │  ❌ Prevent medical diagnosis claims                                  │
 │  ✔ Rephrase with clinical responsibility                              │
 │ Tools: Safety Rules DB, Clinical Guidelines Knowledge Base             │
 └────────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │ Pass (Safe)                   │ Fail (Unsafe) / Warnings
                ▼                                ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                     💊 RECOMMENDATIONS AGENT                          │
 │ Role: Act                                                             │
 │ Tasks: Provide high-level safe suggestions only                       │
 │ Safety: No prescriptions / no diagnoses                               │
 │ Output: Lifestyle suggestions, follow-up reminders, risk alerts       │
 └────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              🟢 Final Output to User (with Clinical Responsibility)
───────────────────────────────────────────────────────────────────────────────
📌 Example Response:
- Simplified medical summary  
- Highlighted abnormal findings  
- Safety warnings (if any)  
- Non-prescriptive recommendations  
───────────────────────────────────────────────────────────────────────────────

```




## 🧩 Agents and Methodology

| Agent | Role | Methodology / Tools |
|-------|------|-------------------|
| ExtractorAgent | Sense | Extract lab values, metrics, diagnoses using **OCR, Regex, NER**, returns structured JSON |
| InterpreterAgent | Plan | Convert extracted values into **patient-friendly interpretation** using Gemini LLM or local model |
| SafetyValidator | Guard | Validates AI output for **clinical safety**, ensures no diagnosis, flags hallucinations |
| RecommenderAgent | Act | Provides **non-prescriptive lifestyle recommendations** (diet, exercise, sleep, hydration) |
| ADKMedAgent | Optional | Provides **additional AI insights** leveraging ADK orchestration and context-aware reasoning |

---

## ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/<username>/medical-report-summarizer.git
cd medical-report-summarizer




---
Create virtual environment & install dependencies:

Create virtual environment & install dependencies:
Add your Gemini API key in a .env file:

GEMINI_API_KEY=your_api_key_here
```bash
---
Run the Streamlit app:
streamlit run app/streamlit_app.py
```bash
