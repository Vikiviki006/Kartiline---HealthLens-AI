"""
Prompt Builder
Builds structured prompt for Gemma.
"""

class PromptBuilder:
    def build_prompt(self, patient: dict, marker: dict, knowledge) -> str:
        knowledge_text = ""
        if knowledge:
            knowledge_text = f"""
            Description: {knowledge.description}
            Low Meaning: {knowledge.low_meaning}
            High Meaning: {knowledge.high_meaning}
            Lifestyle: {knowledge.lifestyle_recommendations}
            Doctor Advice: {knowledge.doctor_advice}
            """
            
        return f"""
        Patient:
        Age: {patient.get("age", "Unknown")}
        Gender: {patient.get("gender", "Unknown")}

        Marker:
        {marker.get("name")}
        Value: {marker.get("value")}
        Reference Range: {marker.get("reference_range")}
        Status: {marker.get("status")}

        Medical Knowledge:
        {knowledge_text}

        Instructions:
        Explain in simple language.
        Do not diagnose.
        Do not create medical facts.
        Use only retrieved medical knowledge.
        Return a short paragraph.
        """

prompt_builder = PromptBuilder()
