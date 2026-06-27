"""
Authentication router - handles login/logout for demo purposes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Demo login endpoint - accepts any email/password combination.
    In production, validate credentials against database.
    """
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")

    # For demo: create a token for any email/password
    # In production: verify password against user in database
    token = create_access_token(subject=request.email)

    return LoginResponse(access_token=token, token_type="bearer")
