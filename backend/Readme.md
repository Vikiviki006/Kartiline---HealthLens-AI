# HealthLens AI — Backend

> **Medical Report Intelligence Platform** — Production-grade FastAPI backend for uploading, OCR-parsing, AI-analysing, and trend-tracking medical reports.

---

## 🚀 Quick Start

### 1. Clone & enter the backend directory
```bash
cd backend
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env — at minimum set DATABASE_URL and GEMINI_API_KEY / OPENAI_API_KEY
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the development server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                     # FastAPI app factory + lifespan hooks
│   │
│   ├── api/
│   │   ├── router.py               # Root API aggregator → /api/v1
│   │   └── v1/
│   │       ├── upload_router.py    # POST  /api/v1/upload
│   │       ├── report_router.py    # GET/DELETE /api/v1/reports[/{id}]
│   │       │                       # POST /api/v1/reports/{id}/analyze
│   │       ├── dashboard_router.py # GET  /api/v1/dashboard
│   │       └── health_router.py    # GET  /api/v1/health[/ping]
│   │
│   ├── controllers/
│   │   ├── upload_controller.py    # Coordinates upload lifecycle
│   │   ├── report_controller.py    # Coordinates report CRUD + analysis
│   │   └── dashboard_controller.py # Coordinates dashboard aggregation
│   │
│   ├── services/
│   │   ├── ocr_service.py          # Multi-engine OCR with fallback
│   │   ├── ai_service.py           # Gemini / OpenAI with retry + JSON parse
│   │   ├── report_service.py       # Report creation + OCR orchestration
│   │   ├── analysis_service.py     # AI analysis orchestration
│   │   ├── dashboard_service.py    # Dashboard aggregation
│   │   └── trend_service.py        # Historical marker trend analysis
│   │
│   ├── repositories/
│   │   ├── report_repository.py    # MedicalReport + ExtractedMarker SQL
│   │   ├── upload_repository.py    # UploadHistory SQL
│   │   ├── user_repository.py      # User SQL
│   │   └── analysis_repository.py  # AIAnalysis SQL
│   │
│   ├── schemas/
│   │   ├── common_schema.py        # Pagination, error, base schemas
│   │   ├── upload_schema.py        # Upload request/response schemas
│   │   ├── report_schema.py        # Report list/detail/marker schemas
│   │   └── dashboard_schema.py     # Dashboard + analysis schemas
│   │
│   ├── models/
│   │   ├── user_model.py           # User ORM model
│   │   ├── report_model.py         # MedicalReport ORM model
│   │   ├── extracted_marker_model.py # ExtractedMarker ORM model
│   │   ├── analysis_model.py       # AIAnalysis ORM model (JSONB fields)
│   │   └── upload_model.py         # UploadHistory ORM model
│   │
│   ├── database/
│   │   ├── base.py                 # DeclarativeBase + UUID/Timestamp/SoftDelete mixins
│   │   ├── session.py              # SQLAlchemy engine + session factory
│   │   └── database.py             # DB init helpers (imports all models)
│   │
│   ├── core/
│   │   ├── config.py               # Pydantic Settings (all env vars)
│   │   ├── constants.py            # Enums, error codes, magic strings
│   │   ├── exceptions.py           # Custom exception hierarchy
│   │   └── security.py             # JWT creation/decoding + password hashing
│   │
│   ├── utils/
│   │   ├── logger.py               # Loguru centralised logger
│   │   ├── response.py             # Standardised JSON response helpers
│   │   ├── validators.py           # File type + size validation
│   │   ├── file_helper.py          # File system utilities
│   │   └── date_helper.py          # Date/time utilities
│   │
│   ├── integrations/
│   │   ├── gemini_client.py        # Gemini SDK wrapper
│   │   ├── openai_client.py        # OpenAI SDK wrapper
│   │   ├── ocr_client.py           # OCR engine availability checks
│   │   └── storage_client.py       # Local / S3 storage abstraction
│   │
│   ├── middleware/
│   │   ├── logging_middleware.py   # Structured per-request logging
│   │   └── exception_middleware.py # Global exception → error envelope
│   │
│   └── tests/
│       ├── test_upload.py
│       ├── test_reports.py
│       └── test_dashboard.py
│
├── alembic/                        # Database migration scripts
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── .env                            # Local secrets (git-ignored)
├── .env.example                    # Template for all env vars
├── requirements.txt
├── alembic.ini
├── pyproject.toml                  # Ruff / Black / mypy / pytest config
└── Dockerfile                      # Multi-stage production image
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/upload` | Upload PDF / image, run OCR, return report |
| `GET` | `/api/v1/reports` | List reports (paginated, filterable, sortable) |
| `GET` | `/api/v1/reports/{id}` | Get full report detail + markers |
| `DELETE` | `/api/v1/reports/{id}` | Soft-delete a report |
| `POST` | `/api/v1/reports/{id}/analyze` | Trigger AI analysis |
| `GET` | `/api/v1/dashboard` | Aggregated dashboard stats + trends |
| `GET` | `/api/v1/health` | Readiness check (DB connectivity) |
| `GET` | `/api/v1/health/ping` | Liveness ping |

### Consistent Response Envelope

**Success:**
```json
{
  "success": true,
  "message": "Request successful",
  "data": { ... },
  "meta": { "page": 1, "page_size": 10, "total": 42, "total_pages": 5 }
}
```

**Error:**
```json
{
  "success": false,
  "message": "Medical report not found: <id>",
  "error_code": "REPORT_NOT_FOUND"
}
```

---

## 🗄️ Database Schema

### Tables
| Table | Description |
|-------|-------------|
| `users` | Authenticated platform users |
| `medical_reports` | Uploaded report files + OCR output |
| `extracted_markers` | Individual health markers from each report |
| `ai_analyses` | AI-generated analysis (1:1 with report) |
| `upload_history` | Audit log of every upload attempt |

All tables share: `id (UUID PK)`, `created_at`, `updated_at`, `is_active`.

---

## 🔧 Environment Variables

See [`.env.example`](.env.example) for the full list. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `SECRET_KEY` | ✅ | JWT signing key (min 32 chars) |
| `AI_PROVIDER` | ✅ | `gemini` or `openai` |
| `GEMINI_API_KEY` | If using Gemini | Google AI API key |
| `OPENAI_API_KEY` | If using OpenAI | OpenAI API key |
| `OCR_ENGINE` | Optional | `pdfplumber` (default), `pymupdf`, `tesseract` |
| `STORAGE_BACKEND` | Optional | `local` (default) or `s3` |

---

## 🐳 Docker

```bash
# Build
docker build -t healthlens-api .

# Run
docker run -p 8000:8000 --env-file .env healthlens-api
```

---

## 🧪 Testing

```bash
pytest app/tests/ -v
```

---

## 🗂️ Database Migrations (Alembic)

```bash
# Create a new migration
alembic revision --autogenerate -m "add_new_column"

# Apply all migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View migration history
alembic history
```

---

## 🔒 Security

- **JWT authentication** — Bearer token on all protected routes
- **Password hashing** — bcrypt via Passlib
- **CORS** — configurable origins via `CORS_ORIGINS`
- **Input validation** — file type, size, and Pydantic schema validation
- **Soft deletes** — records never truly deleted; `is_active=False`
- **Non-root Docker user** — `healthlens` user in container

---

## 🛠️ Code Quality

```bash
# Format
black app/

# Lint
ruff check app/

# Type check
mypy app/
```

---

## 📈 Production Checklist

- [ ] Set `APP_ENV=production` (disables Swagger UI)
- [ ] Set a strong `SECRET_KEY` (`openssl rand -hex 32`)
- [ ] Use `STORAGE_BACKEND=s3` with proper IAM permissions
- [ ] Configure `CORS_ORIGINS` to your frontend domain only
- [ ] Set `LOG_LEVEL=WARNING` to reduce log volume
- [ ] Deploy with at least 2 Uvicorn workers per CPU core
- [ ] Put behind a reverse proxy (Nginx / Caddy) with TLS
- [ ] Set up Alembic migration CI step before deployment
- [ ] Configure database connection pooling (PgBouncer recommended)
