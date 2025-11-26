# agents/orchestrator.py
from agents.extractor_agent import ExtractorAgent
from agents.interpreter_agent import InterpreterAgent
from agents.safety_agent import SafetyAgent
from agents.recommender_agent import RecommenderAgent

class Orchestrator:
    def __init__(self, mode="offline"):
        # mode can be "offline" or "online" (to be extended)
        self.mode = mode
        self.extractor = ExtractorAgent()
        self.interpreter = InterpreterAgent()
        self.safety = SafetyAgent()
        self.recommender = RecommenderAgent()

    def run_pipeline(self, report_text: str, sex="all"):
        extracted_resp = self.extractor.run(report_text)
        extracted = extracted_resp.get("extracted", [])
        interpreted = self.interpreter.run(extracted, sex=sex)

        # Build raw summary
        parts = []
        for it in interpreted:
            parts.append(f"{it['name'].title()}: {it['status']} - {it['explanation']}")
        raw_summary = "\n".join(parts)

        # Safety validation
        safe_summary = self.safety.run(raw_summary)

        # Recommendations
        recs = self.recommender.run(interpreted)

        return {
            "extracted": extracted,
            "interpreted": interpreted,
            "raw_summary": raw_summary,
            "safe_summary": safe_summary,
            "recommendations": recs
        }
