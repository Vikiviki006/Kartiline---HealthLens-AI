import os
import glob

def replace_in_files(directory, replacements):
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith('.py'):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
                
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {path}")

replacements = {
    "MedicalReport": "Report",
    "ExtractedMarker": "ReportMarker",
    "extracted_marker_model": "report_marker_model",
    "AIAnalysis": "MarkerAnalysis",
    "analysis_model": "marker_analysis_model",
    "MarkerSeverity.ABNORMAL.value": '"High"', # update severity to status
    "MarkerSeverity.CRITICAL.value": '"Critical"',
    ".severity": ".status"
}

replace_in_files("app", replacements)
