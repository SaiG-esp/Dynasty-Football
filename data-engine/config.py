"""Shared configuration for data-engine scripts.

Loads the CollegeFootballData API key from the environment (or a local
.env file, see .env.example) instead of hardcoding it in every script.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("CFBD_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "CFBD_API_KEY is not set. Copy data-engine/.env.example to "
        "data-engine/.env and add your CollegeFootballData API key."
    )

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
