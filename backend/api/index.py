"""
Vercel Serverless Entrypoint for FastAPI application.
Exposes the main FastAPI instance for Vercel deployment.
"""

import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

__all__ = ["app"]
