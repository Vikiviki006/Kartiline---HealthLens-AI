"""
Custom exception hierarchy for HealthLens AI.

All domain-specific errors subclass AppException which carries:
  - HTTP status code
  - Human-readable message
  - Machine-readable error_code
  - Optional extra context
"""

from typing import Any

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base class for all HealthLens exceptions."""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str,
        detail: Any = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.error_code = error_code
        self.extra = detail


# ── 400 Bad Request ───────────────────────────────────────────────────────────

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", error_code: str = "BAD_REQUEST", detail: Any = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, error_code, detail)


class InvalidFileTypeException(AppException):
    def __init__(self, filename: str = ""):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"Invalid file type: '{filename}'. Only PDF and image files are accepted.",
            "INVALID_FILE_TYPE",
        )


class FileTooLargeException(AppException):
    def __init__(self, max_mb: int = 20):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"File exceeds the maximum allowed size of {max_mb} MB.",
            "FILE_TOO_LARGE",
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed", detail: Any = None):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message, "VALIDATION_ERROR", detail)


# ── 401 Unauthorized ──────────────────────────────────────────────────────────

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, "UNAUTHORIZED")


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid email or password.",
            "INVALID_CREDENTIALS",
        )


class TokenExpiredException(AppException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Token has expired.", "TOKEN_EXPIRED")


class TokenInvalidException(AppException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Token is invalid.", "TOKEN_INVALID")


# ── 403 Forbidden ─────────────────────────────────────────────────────────────

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(status.HTTP_403_FORBIDDEN, message, "FORBIDDEN")


# ── 404 Not Found ─────────────────────────────────────────────────────────────

class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", resource_id: str = ""):
        msg = f"{resource} not found" + (f": {resource_id}" if resource_id else "")
        code = resource.upper().replace(" ", "_") + "_NOT_FOUND"
        super().__init__(status.HTTP_404_NOT_FOUND, msg, code)


class ReportNotFoundException(AppException):
    def __init__(self, report_id: str = ""):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"Medical report not found" + (f": {report_id}" if report_id else ""),
            "REPORT_NOT_FOUND",
        )


class UserNotFoundException(AppException):
    def __init__(self, user_id: str = ""):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"User not found" + (f": {user_id}" if user_id else ""),
            "USER_NOT_FOUND",
        )


class AnalysisNotFoundException(AppException):
    def __init__(self, report_id: str = ""):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"Analysis not found for report: {report_id}",
            "ANALYSIS_NOT_FOUND",
        )


# ── 409 Conflict ──────────────────────────────────────────────────────────────

class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists", error_code: str = "CONFLICT"):
        super().__init__(status.HTTP_409_CONFLICT, message, error_code)


class UserAlreadyExistsException(AppException):
    def __init__(self, email: str = ""):
        super().__init__(
            status.HTTP_409_CONFLICT,
            f"A user with email '{email}' already exists.",
            "USER_ALREADY_EXISTS",
        )


# ── 500 Internal Server Error ─────────────────────────────────────────────────

class InternalServerException(AppException):
    def __init__(self, message: str = "An unexpected error occurred"):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR, message, "INTERNAL_SERVER_ERROR"
        )


class OCRFailedException(AppException):
    def __init__(self, detail: str = ""):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"OCR processing failed" + (f": {detail}" if detail else ""),
            "OCR_FAILED",
        )


class AIServiceException(AppException):
    def __init__(self, detail: str = ""):
        super().__init__(
            status.HTTP_502_BAD_GATEWAY,
            f"AI service error" + (f": {detail}" if detail else ""),
            "AI_SERVICE_ERROR",
        )


class AITimeoutException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_504_GATEWAY_TIMEOUT,
            "AI service timed out. Please try again.",
            "AI_TIMEOUT",
        )


class UploadFailedException(AppException):
    def __init__(self, detail: str = ""):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"File upload failed" + (f": {detail}" if detail else ""),
            "UPLOAD_FAILED",
        )
