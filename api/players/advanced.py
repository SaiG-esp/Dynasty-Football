"""Vercel serverless: GET /api/players/advanced

Proxies CollegeFootballData server-side so the browser never holds CFBD_API_KEY.
Reuses data-engine advanced_stats / cfbd_client logic.
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Make data-engine importable when this function is bundled on Vercel.
_ROOT = Path(__file__).resolve().parents[2]
_DATA_ENGINE = _ROOT / "data-engine"
if str(_DATA_ENGINE) not in sys.path:
    sys.path.insert(0, str(_DATA_ENGINE))


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _handle_advanced(query: dict) -> tuple[int, dict]:
    import os

    # Strip whitespace/newlines — cloud secrets sometimes include a trailing \n.
    api_key = (os.environ.get("CFBD_API_KEY") or "").strip()
    if not api_key:
        return 503, {"detail": "CFBD_API_KEY is not configured on the server"}

    # Ensure config.API_KEY reflects the cleaned value for this request.
    import config

    config.API_KEY = api_key

    name = (query.get("name") or [""])[0].strip()
    school = (query.get("school") or [""])[0].strip()
    position = (query.get("position") or [""])[0].strip()
    year_raw = (query.get("year") or [None])[0]

    if not name or not school:
        return 400, {"detail": "name and school are required"}

    try:
        year = int(year_raw) if year_raw not in (None, "") else int(
            os.environ.get("DEFAULT_SCOUT_YEAR", "2025")
        )
    except ValueError:
        return 400, {"detail": "year must be an integer"}

    from advanced_stats import build_advanced_stats
    from cfbd_client import CfbdError

    try:
        rows = build_advanced_stats(name, school, position, year)
        return 200, {
            "player": name,
            "school": school,
            "position": position,
            "year": year,
            "games": rows,
        }
    except ValueError as e:
        return 400, {"detail": str(e)}
    except CfbdError as e:
        status = e.status_code if e.status_code in (401, 429) else 502
        return status, {"detail": str(e)}
    except Exception as e:
        return 500, {"detail": f"Advanced stats failed: {e}"}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        status, payload = _handle_advanced(query)
        _json_response(self, status, payload)

    def log_message(self, format, *args):  # noqa: A003 — silence default access logs
        return
