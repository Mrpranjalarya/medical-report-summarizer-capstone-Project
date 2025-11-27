# agents/recommender_agent.py

RECOMMENDATIONS = {
    "hemoglobin": {
        "low": [
            "Increase dietary iron (spinach, legumes).",
            "Ask clinician about iron supplementation if needed."
        ],
        "high": [
            "High hemoglobin may require medical evaluation.",
            "Stay hydrated and monitor changes."
        ],
        "normal": [
            "Maintain a balanced intake of iron-rich foods and stay hydrated."
        ]
    },
    "cholesterol": {
        "high": [
            "Reduce saturated fats and increase fiber.",
            "Schedule a follow-up lipid panel and clinician consultation."
        ],
        "normal": [
            "Continue a heart-healthy diet and regular exercise."
        ]
    },
    "glucose": {
        "high": [
            "Reduce simple carbohydrates and sugary foods.",
            "Schedule fasting blood glucose test and clinician screening."
        ],
        "normal": [
            "Maintain balanced meals and regular physical activity."
        ]
    }
}

GENERAL_HEALTH_RECOMMENDATION = (
    "Maintain a balanced diet, regular exercise, and follow-up with your healthcare provider."
)


class RecommenderAgent:
    def __init__(self):
        pass

    def run(self, interpreted):
        """
        interpreted → list of dicts:
        [
            {"name": "hemoglobin", "status": "low", "value": 10.2, ...},
            {"name": "cholesterol", "status": "high", "value": 242, ...}
        ]
        """
        final_recs = []

        for it in interpreted:
            name = (it.get("name") or "").lower()
            status = (it.get("status") or "").lower()

            if not name or not status:
                continue

            rules = RECOMMENDATIONS.get(name, {})
            category_recs = rules.get(status, [])

            if category_recs:
                final_recs.append({
                    "marker": name,
                    "status": status,
                    "recommendations": list(set(category_recs))  # remove duplicates if any
                })

        # If nothing matched → general well-being advice
        if not final_recs:
            final_recs.append({
                "marker": "general",
                "status": "neutral",
                "recommendations": [GENERAL_HEALTH_RECOMMENDATION]
            })

        return final_recs
