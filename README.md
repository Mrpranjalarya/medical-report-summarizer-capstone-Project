# 🧠 AI Medical Summary Assistant

**Medical Report Summarizer & Patient Support System**  
Built with Google Gemini (LLM), Local Models (optional), and a modular multi-agent architecture.

---

## 🔹 Project Overview – ADK-MedAgent

ADK-MedAgent is a multi-agent system designed to read, interpret, and summarize medical reports. It analyzes uploaded blood reports and provides explanations in simple language, detects abnormal values, and recommends improvements based on medical guidelines.

This project introduces AI Medical Summary Assistant, a multi-agent ADK-powered system that extracts, interprets, and validates key insights from medical reports with safety and clinical responsibility.

- Orchestrates and coordinates all agents using a central ADK brain
- Extracts medical values and findings
- Interprets them in patient-friendly language
- Validates safety and clinical responsibility
- Provides non-prescriptive lifestyle recommendations
- Generates optional AI insights via ADK agent

🩺 Problem Statement

Medical lab reports contain complex medical terminology that is difficult for non-medical users to understand.
Patients struggle with:

Interpreting medical parameters

Identifying whether values are normal or risky

Understanding what lifestyle or medication changes are needed

Doctors do not have time to manually explain every report, so patients often leave confused, anxious, or misinformed.

---
```bash
## 📂 Project Structure

medical-report-summarizer/
├── .venv/ # Python virtual environment
├── agents/ # AI agents:orchestrator, Extractor, Interpreter, Recommender, Safety, ADK
├── app/ # Streamlit UI
├── data/ # Sample reports and datasets
├── docs/ # Documentation & flowcharts
├── memory/ # Session service and memory storage
├── tests/ # Unit tests
└── tools/ # Utility scripts


```
```mermaid

graph TD
    A[🧠ADK Orchestrator(Brain)] --> B[📄 Extractor Agent]
    A --> C[🗣 Interpreter Agent]
    A --> D[💡 Recommendation Agent]
    A --> E[🛡 Safety Validator Agent]
    A --> F[🔍 Optional ADK Medical Insights Agent]

    subgraph Extract Phase
        B --> B1((OCR))
        B --> B2((Regex Parsing))
        B --> B3((NER Medical Entity Extraction))
    end

    subgraph Interpret Phase
        C --> C1((Gemini LLM / Local Model))
        C --> C2((Context Memory))
    end

    subgraph Recommendation Phase
        D --> D1((Lifestyle Guidance))
        D --> D2((Diet – Sleep – Exercise – Hydration Tips))
    end

    subgraph Validation Phase
        E --> E1((Clinical Safety Check))
        E --> E2((No Diagnosis / No Prescription))
        E --> E3((Hallucination Detection))
    end

    subgraph Optional ADK Insights
        F --> F1((Pattern-Based Insights))
        F --> F2((Future Health Risk Factors – Non Medical))
    end

    %% Workflow Loop
    E -->|⚠ If Unsafe| C
    E -->|⚠ If Missing Info| B
    E -->|✔ Approved| A
    A -->|Final Output| Z[📦 Final Medical Summary Report]


```


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
| **ADK Orchestrator (Brain)** | Control | Manages **execution flow**, agent delegation, context & memory, tools routing |
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
```
🏁 Conclusion

AI Medical Summary Assistant proves how multi-agent ADK systems can accelerate healthcare workflows while ensuring accuracy, safety, and interpretability. The modular agent approach also makes the system highly scalable and future-ready.

📎 Acknowledgements

Special thanks to Google ADK & Kaggle Agents Intensive community for guidance and sample architecture references.
