# AI Medical Report Summarizer & Patient Support (Streamlit)

**Purpose:** A local-first Streamlit app that extracts and explains common lab report values,
classifies them against reference ranges, and provides safe, conservative lifestyle recommendations.

**Features**
- Multi-agent architecture (extractor, interpreter, recommender, safety)
- Streamlit UI for pasting/uploading reports (text & basic PDF text extraction)
- Session memory for simple trend comparisons (JSON file)
- Local-only implementation (no external OCR APIs required)

## Quick start (local)
1. Create a Python 3.11+ virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app/streamlit_app.py
   ```

**Notes**
- This project is for educational/demo purposes. It is NOT medical advice.
- For PDF reports, `pdfplumber` is used to extract text; highly-scanned images may not extract well without OCR.