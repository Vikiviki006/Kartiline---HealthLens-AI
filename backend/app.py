"""
HealthLens AI — Root Application Entrypoint for local running and Vercel serverless functions.
"""

import os
import sys

# Ensure backend root directory is in sys.path for Vercel and local runners
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

__all__ = ["app"]