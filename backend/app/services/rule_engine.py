"""
Python Rule Engine
Parses reference ranges and compares marker values to determine status.
"""

class RuleEngine:
    def determine_status(self, name: str, value: float, reference_range: str) -> str:
        if not reference_range or not value:
            return "Unknown"
        try:
            if "-" in reference_range:
                min_val, max_val = map(float, reference_range.split("-"))
                if value < min_val: return "Low"
                if value > max_val: return "High"
                return "Normal"
            elif "<" in reference_range:
                max_val = float(reference_range.replace("<", "").strip())
                if value > max_val: return "High"
                return "Normal"
            elif ">" in reference_range:
                min_val = float(reference_range.replace(">", "").strip())
                if value < min_val: return "Low"
                return "Normal"
        except:
            pass
        return "Unknown"

    def process_markers(self, markers: list[dict]) -> list[dict]:
        for m in markers:
            try:
                val = float(m.get("value", 0))
                m["status"] = self.determine_status(m.get("name", ""), val, m.get("reference_range", ""))
            except:
                m["status"] = "Unknown"
        return markers

rule_engine = RuleEngine()
