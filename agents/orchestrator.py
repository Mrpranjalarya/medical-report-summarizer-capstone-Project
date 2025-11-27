# agents/orchestrator.py
from agents.extractor_agent import ExtractorAgent
from agents.interpreter_agent import InterpreterAgent
from agents.safety_agent import SafetyAgent
from agents.recommender_agent import RecommenderAgent


class Orchestrator:
    def __init__(self, mode="offline"):
        """
        Orchestrates the complete pipeline of:
        1) Extraction
        2) Interpretation
        3) Safety Check
        4) Recommendations
        """
        self.mode = mode
        self.extractor = ExtractorAgent()
        self.interpreter = InterpreterAgent()
        self.safety = SafetyAgent()
        self.recommender = RecommenderAgent()

    def run_pipeline(self, report_text: str, sex="all"):
        if not report_text or not report_text.strip():
            return {
                "error": True,
                "message": "Report text is empty",
                "extracted": [],
                "interpreted": [],
                "raw_summary": "",
                "safe_summary": "",
                "recommendations": []
            }

        try:
            # Step 1: Extract structured values
            extracted_resp = self.extractor.run(report_text)
            extracted = extracted_resp.get("extracted", [])

            # Step 2: Interpret values (Low / High / Normal)
            interpreted = self.interpreter.run(extracted, sex=sex)

            # Step 3: Create human-readable summary
            raw_summary = "\n".join(
                f"{i['name'].title()}: {i['status']} — {i['explanation']}"
                for i in interpreted
            )

            # Step 4: Safety re-check (remove harmful medical claims)
            safe_summary = self.safety.run(raw_summary)

            # Step 5: Lifestyle / diet recommendations
            recommendations = self.recommender.run(interpreted)

            return {
                "error": False,
                "extracted": extracted,
                "interpreted": interpreted,
                "raw_summary": raw_summary,
                "safe_summary": safe_summary,
                "recommendations": recommendations
            }

        except Exception as e:
            # Protect backend from crashing due to any agent failure
            return {
                "error": True,
                "message": f"Pipeline failed: {str(e)}",
                "extracted": [],
                "interpreted": [],
                "raw_summary": "",
                "safe_summary": "",
                "recommendations": []
            }
