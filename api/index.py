"""Vercel serverless entrypoint.

Vercel's Python runtime looks for a WSGI callable named `app` in this file.
The real application lives in backend/app.py, so this just puts that folder on
the import path and re-exports it - there is no second copy of the code.
"""

import os
import sys

BACKEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import app  # noqa: E402  (must come after the sys.path tweak)

# Vercel invokes this WSGI application directly; app.run() is never called.
__all__ = ["app"]
