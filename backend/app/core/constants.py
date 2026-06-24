"""
Application-wide constants.
Keep all magic strings, numeric limits, and enum-like values here.
"""

from enum import Enum


# ── File handling ─────────────────────────────────────────────────────────────

ALLOWED_MIME_TYPES: set[str] = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/tiff",
}

PDF_MIME_TYPE = "application/pdf"


# ── Report status ─────────────────────────────────────────────────────────────

class ReportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ── Analysis status ───────────────────────────────────────────────────────────

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ── Marker severity ───────────────────────────────────────────────────────────

class MarkerSeverity(str, Enum):
    NORMAL = "normal"
    BORDERLINE = "borderline"
    ABNORMAL = "abnormal"
    CRITICAL = "critical"


# ── User roles ────────────────────────────────────────────────────────────────

class UserRole(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


# ── Pagination ────────────────────────────────────────────────────────────────

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
MIN_PAGE = 1


# ── Error codes ───────────────────────────────────────────────────────────────

class ErrorCode(str, Enum):
    # Generic
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    BAD_REQUEST = "BAD_REQUEST"

    # Auth
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"

    # Upload
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UPLOAD_FAILED = "UPLOAD_FAILED"

    # Report
    REPORT_NOT_FOUND = "REPORT_NOT_FOUND"
    REPORT_PROCESSING = "REPORT_PROCESSING"

    # OCR
    OCR_FAILED = "OCR_FAILED"
    OCR_EMPTY_RESULT = "OCR_EMPTY_RESULT"

    # AI
    AI_SERVICE_ERROR = "AI_SERVICE_ERROR"
    AI_PARSE_ERROR = "AI_PARSE_ERROR"
    AI_TIMEOUT = "AI_TIMEOUT"

    # Analysis
    ANALYSIS_NOT_FOUND = "ANALYSIS_NOT_FOUND"
    ANALYSIS_ALREADY_EXISTS = "ANALYSIS_ALREADY_EXISTS"


# ── AI prompt keys ────────────────────────────────────────────────────────────

class PromptKey(str, Enum):
    HEALTH_SUMMARY = "health_summary"
    ABNORMAL_MARKERS = "abnormal_markers"
    RECOMMENDATIONS = "recommendations"
    DOCTOR_QUESTIONS = "doctor_questions"
    TREND_ANALYSIS = "trend_analysis"
