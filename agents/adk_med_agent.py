# agents/adk_med_agent.py

import json
from typing import Dict, Any

class ADKMedAgent:
    """
    ADK Medical Insight Agent
    Purpose:
    - Reason over extracted medical facts
    - Identify patterns / risk factors
    - Suggest high-level safe insights without diagnosis
    """

    def __init__(self, model=None):
        """
        model: pass Gemini / OpenAI / local LLM instance
        If None → fallback to rule-based insights
        """
        self.model = model
        self.agent_name = "ADKMedAgent"

    def _rule_based_insights(self, facts: Dict[str, Any]) -> list:
        """Fallback reasoning without LLM"""
        insights = []
        cholesterol = facts.get("LDL") or facts.get("cholesterol")
        sugar = facts.get("HbA1c") or facts.get("blood_sugar")

        if cholesterol and cholesterol > 160:
            insights.append("Possible cardiovascular risk if LDL remains elevated long-term.")
        if sugar and sugar > 6.4:
            insights.append("Blood sugar is above healthy range. May indicate risk of diabetes progression.")
        if not insights:
            insights.append("No major risk patterns detected from available report values.")

        return insights

    def _llm_insights(self, facts: Dict[str, Any]) -> list:
        """Use LLM for reasoning if available"""
        prompt = f"""
        You are a medical insight AI providing safe clinical observations.
        Facts: {facts}

        Produce 3 bullet insights about risk patterns WITHOUT diagnosing disease or prescribing medicine.
        Tone: neutral + educational.
        """
        response = self.model.generate(prompt)  # supports Gemini / HuggingFace / OpenAI wrapper
        return response.strip().split("\n")

    def run(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: structured facts (dict)
        Output: safe structured insights (dict)
        """
        if not isinstance(facts, dict) or not facts:
            return {"agent": self.agent_name, "insights": [], "note": "No structured data provided"}

        # Use LLM if passed, else rules
        if self.model:
            insights = self._llm_insights(facts)
        else:
            insights = self._rule_based_insights(facts)

        # Safety wording enforcement
        safe_insights = [
            f"- {line.replace('you have', 'there may be').replace('diagnose', 'suggests monitoring')}"
            for line in insights if line
        ]

        return {
            "agent": self.agent_name,
            "insights": safe_insights,
            "source": "LLM" if self.model else "Rule-Based",
        }
