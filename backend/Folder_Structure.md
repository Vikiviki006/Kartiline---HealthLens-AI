# 📁 Project Structure

```text
HealthLens-AI/
│
├── README.md
├── IDEA_ANALYSIS.md
├── PROJECT_STRUCTURE.md
├── PITCH_DECK.md
├── SYSTEM_ARCHITECTURE.md
├── API_DOCUMENTATION.md
├── DATABASE_SCHEMA.md
├── ROADMAP.md
├── LICENSE
│
├── frontend/
│   ├── public/
│   │   ├── icons/
│   │   └── images/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadSection/
│   │   │   ├── HealthDashboard/
│   │   │   ├── TrendAnalysis/
│   │   │   └── DoctorSummary/
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── History.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── reportService.js
│   │   │
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── assets/
│   │
│   └── package.json
│
├── backend/
│   ├── app.py
│   │
│   ├── api/
│   │   ├── upload.py
│   │   ├── reports.py
│   │   ├── trends.py
│   │   └── summary.py
│   │
│   ├── ai_engine/
│   │   ├── marker_explainer.py
│   │   ├── trend_analyzer.py
│   │   ├── risk_detector.py
│   │   └── doctor_assistant.py
│   │
│   ├── ocr/
│   │   ├── pdf_parser.py
│   │   └── image_extractor.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── report.py
│   │   └── marker.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── schema.sql
│   │
│   └── utils/
│
├── docs/
│   ├── architecture.png
│   ├── workflow.png
│   ├── user_journey.png
│   ├── dashboard_mockup.png
│   └── future_roadmap.png
│
├── sample_reports/
│   ├── blood_test_sample.pdf
│   ├── thyroid_report_sample.pdf
│   └── lipid_profile_sample.pdf
│
└── tests/
    ├── test_ocr.py
    ├── test_api.py
    └── test_ai_engine.py
```

## Structure Overview

### Frontend

Responsible for:

* Report Upload Interface
* Health Dashboard
* Trend Visualization
* Doctor Summary Display

### Backend

Responsible for:

* OCR Processing
* AI Analysis
* Risk Detection
* Report Management
* API Services

### AI Engine

Core intelligence layer that:

* Explains medical markers
* Detects abnormalities
* Tracks health trends
* Generates consultation summaries

### Docs

Contains:

* System Architecture
* Workflow Diagrams
* UI Mockups
* User Journey Maps

### Sample Reports

Used for:

* Development
* Testing
* Demonstrations

### Tests

Ensures:

* OCR accuracy
* API reliability
* AI output validation

```
```
