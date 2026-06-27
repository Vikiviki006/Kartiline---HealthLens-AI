# 🩺 HealthLens AI

> **Understand Your Health Before Your Appointment**

HealthLens AI is an AI-powered Medical Report Intelligence Platform that transforms complex laboratory reports into easy-to-understand health insights using OCR, Artificial Intelligence, and historical trend analysis.

Instead of replacing medical professionals, HealthLens empowers patients to better understand their reports, prepare for doctor consultations, and monitor their long-term health.

---

# 🎥 Demo

> Add your project demo video here.

```text
🎬 Demo Video
[https://github.com/user-attachments/assets/your-video-link](https://drive.google.com/file/d/1t1hRiTi6brqczITpau9klfRAwQjLZYg1/view?usp=sharing)
```


---

# 🚀 Problem Statement

Millions of people receive blood tests, health screenings, and diagnostic reports every year.

Unfortunately:

* Medical reports are difficult for non-medical users to understand.
* Medical abbreviations create confusion.
* Important abnormalities are often overlooked.
* Patients become anxious before consulting doctors.
* Tracking health improvements across reports is difficult.

HealthLens AI solves these problems by converting complex reports into personalized, easy-to-understand explanations.

---

# 💡 Solution

HealthLens AI allows users to upload medical reports and instantly receive:

* 📄 OCR-based report extraction
* 🤖 AI-generated health explanations
* ⚠️ Abnormal marker detection
* 📈 Historical health trend analysis
* 💬 AI chat assistant
* 📝 Doctor visit preparation
* 📊 Personal health dashboard

The platform is educational and does **not** diagnose diseases.

---

# ✨ Key Features

## 📄 Smart Report Upload

Supports:

* PDF
* JPG
* PNG
* TIFF

with automatic validation and OCR processing.

---

## 🤖 AI Medical Explanation

Explains:

* Medical terminology
* Blood markers
* Reference ranges
* Health significance

using Large Language Models.

---

## ⚠️ Abnormal Marker Detection

Automatically detects

* Low values
* High values
* Critical markers

and explains why they matter.

---

## 📈 Health Trend Analysis

Compare multiple reports over time.

Visualize improvements or deteriorations in:

* Hemoglobin
* Glucose
* Cholesterol
* Platelets
* Thyroid markers
* Liver markers

---

## 💬 AI Chat Assistant

Users can ask questions like:

> Why is my cholesterol high?

> What does low hemoglobin mean?

> Should I discuss Vitamin D with my doctor?

---

## 📝 Doctor Visit Preparation

Generates:

* Health summary
* Doctor questions
* Important discussion points
* Follow-up recommendations

---

# 🏗️ System Architecture

```text
                Medical Report
                      │
                      ▼
              Upload Interface
                      │
                      ▼
                OCR Extraction
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Structured Medical Data      Raw OCR Text
        │                           │
        └─────────────┬─────────────┘
                      ▼
              AI Analysis Engine
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Marker Insights   Health Trends   Doctor Questions
      │               │                │
      └───────────────┴────────────────┘
                      ▼
             Health Dashboard
```

---

# ⚙️ Technology Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Axios
* Recharts

---

## Backend

* FastAPI
* Python
* SQLAlchemy
* Alembic
* JWT Authentication

---

## Artificial Intelligence

* OpenAI API
* Gemini API
* Prompt Engineering
* Medical Report Intelligence

---

## OCR

* Tesseract OCR
* PDF Processing
* Image Processing

---

## Database

* PostgreSQL

---

## Storage

* AWS S3
* Cloudinary

---

## Deployment

* Vercel
* Render

---

# 📂 Project Structure

```text
HealthLens-AI

frontend/
    Next.js Application

backend/
    FastAPI Application

database/
    PostgreSQL

uploads/
    Medical Reports

README.md
```

---

# 🔄 User Workflow

```text
User Login
      │
      ▼
Upload Medical Report
      │
      ▼
OCR Extracts Report
      │
      ▼
Medical Markers Stored
      │
      ▼
AI Generates Explanation
      │
      ▼
Dashboard Updates
      │
      ▼
Health Trends Generated
      │
      ▼
Doctor Preparation Created
      │
      ▼
Chat with AI
```

---

# 🌐 API Overview

| Method | Endpoint              | Description    |
| ------ | --------------------- | -------------- |
| POST   | /upload               | Upload report  |
| GET    | /reports              | Get reports    |
| GET    | /reports/{id}         | Report details |
| POST   | /reports/{id}/analyze | AI Analysis    |
| DELETE | /reports/{id}         | Delete report  |
| GET    | /dashboard            | Dashboard      |

---

# 🔒 Security

* JWT Authentication
* Password Hashing
* Protected APIs
* Input Validation
* Secure File Upload
* CORS Protection

---

# 📊 Dashboard

Users can monitor

* Total Reports
* Processing Reports
* Completed Reports
* Abnormal Reports
* Historical Trends
* AI Insights

---

# 🧠 AI Capabilities

HealthLens AI can

* Explain blood markers
* Detect abnormalities
* Summarize reports
* Compare reports
* Generate doctor questions
* Answer user queries
* Produce personalized health summaries

---

# 🚀 Future Enhancements

* Multi-language Support
* Voice Assistant
* Mobile App
* Family Health Dashboard
* Specialist Recommendation
* Wearable Integration
* Health Score
* Appointment Scheduling

---

# ⚡ Quick Start

## Backend

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Backend runs on

```
http://localhost:8000
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on

```
http://localhost:3000
```

---

# 📈 Impact

HealthLens AI helps users

* Understand medical reports in seconds
* Reduce confusion
* Prepare for doctor consultations
* Track long-term health
* Improve health awareness

---

# ⚠️ Disclaimer

HealthLens AI is intended for educational and informational purposes only.

It does not provide medical diagnosis, treatment recommendations, or professional medical advice. Users should always consult qualified healthcare professionals regarding medical decisions.

---

# 👨‍💻 Team Vision

> **"Your health data should be understandable, not intimidating."**

Our mission is to bridge the gap between complex medical information and patient understanding through Artificial Intelligence, making healthcare more accessible, transparent, and empowering for everyone.
