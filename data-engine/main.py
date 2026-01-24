from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# --- NEW: SECURITY PASS ---
# This allows your React site (localhost:5173) to talk to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Config
DB_CONFIG = {
    "dbname": "postgres",
    "user": "jarvis",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynasty Football API! 🏈"}

@app.get("/defenses")
def get_all_defenses():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM defensive_intel ORDER BY havoc_score DESC")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows