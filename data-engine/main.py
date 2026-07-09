import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import DB_CONFIG

app = FastAPI(title="Dynasty Football API")

# Comma-separated list of allowed origins, e.g. "http://localhost:5173,https://myapp.com"
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
ALLOWED_ORIGINS = [
    o.strip() for o in os.environ.get("ALLOWED_ORIGINS", _default_origins).split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynasty Football API! 🏈"}


@app.get("/health")
def health_check():
    """Lightweight readiness check: confirms the API can reach Postgres."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database unreachable")
    conn.close()
    return {"status": "ok"}


@app.get("/defenses")
def get_all_defenses():
    """Returns every team's defensive havoc rating, most recently updated
    first tie-broken by havoc_score. Populated by data-engine/matchup_data3.py."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM defensive_intel ORDER BY havoc_score DESC")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
    finally:
        conn.close()


@app.get("/defenses/{team_name}")
def get_defense(team_name: str):
    """Returns a single team's defensive havoc rating (case-insensitive)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT * FROM defensive_intel WHERE LOWER(team_name) = LOWER(%s)",
            (team_name,),
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            raise HTTPException(status_code=404, detail=f"No defensive data for '{team_name}'")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
    finally:
        conn.close()
