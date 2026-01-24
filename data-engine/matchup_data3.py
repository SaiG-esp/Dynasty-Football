import requests
import warnings
import psycopg2
from psycopg2.extras import execute_values
from dateutil import parser

# 1. SETUP & CONFIGURATION
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }
YEAR = 2024

# Database Config (Matches your Local Setup)
DB_CONFIG = {
    "dbname": "postgres",
    "user": "jarvis",
    "password": "",  # Leave empty since you have no password
    "host": "localhost",
    "port": "5432"
}

# --- CACHE FOR DEFENSIVE STATS ---
OPPONENT_INTEL = {}

def prefetch_defensive_intel():
    """
    Fetches stats for ALL teams in 2024.
    Tracks: TFL, Sacks, INT, PD, and Fumbles Recovered.
    """
    print(f"🛡️  Scouting all FBS defenses for {YEAR}...", end="\r")
    
    # 1. Get Game Counts
    games_played = {}
    try:
        rec_url = "https://api.collegefootballdata.com/records"
        rec_resp = requests.get(rec_url, headers=HEADERS, params={"year": YEAR})
        for team in rec_resp.json():
            g_count = team['total']['games']
            games_played[team['team']] = max(1, g_count)
    except: pass

    # 2. Get Raw Stats
    stats_url = "https://api.collegefootballdata.com/stats/season"
    try:
        resp = requests.get(stats_url, headers=HEADERS, params={"year": YEAR})
        data = resp.json()
        
        for row in data:
            team = row['team']
            stat = row['statName']
            val = row['statValue']
            
            if team not in OPPONENT_INTEL:
                OPPONENT_INTEL[team] = {
                    'tfl': 0, 'sacks': 0, 'int': 0, 'pd': 0, 'fumbles': 0, 
                    'games': games_played.get(team, 1)
                }
            
            if stat == 'tacklesForLoss': OPPONENT_INTEL[team]['tfl'] = val
            elif stat == 'sacks': OPPONENT_INTEL[team]['sacks'] = val
            elif stat == 'interceptions': OPPONENT_INTEL[team]['int'] = val
            elif stat == 'passesDeflected': OPPONENT_INTEL[team]['pd'] = val
            elif stat == 'fumblesRecovered': OPPONENT_INTEL[team]['fumbles'] = val

    except: 
        print("\n⚠️ Failed to fetch defensive stats.")
        return

    print("✅ Defensive Intel Loaded from API.       ")

def update_database():
    """
    Takes the raw data from OPPONENT_INTEL, calculates the Havoc Scores,
    and saves them into your PostgreSQL database.
    """
    print(f"💾 Saving intel to the Database...", end="\r")
    
    try:
        # 1. Connect to Database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        rows_to_insert = []
        
        # 2. Calculate Stats for Every Team
        for team, stats in OPPONENT_INTEL.items():
            g = stats['games']
            if g == 0: continue
            
            # Havoc Formula: (TFL + 2*Int + 2*Fum + 1.5*Sacks + PD) / Games
            tfl = stats['tfl']
            ints = stats['int']
            fums = stats['fumbles']
            sacks = stats['sacks']
            pd = stats['pd']
            
            weighted_sum = tfl + (2 * ints) + (2 * fums) + (1.5 * sacks) + pd
            havoc_score = weighted_sum / g
            sacks_pg = sacks / g
            turnovers_pg = (ints + fums) / g
            
            # Prepare row: (Team, Havoc, Sacks, Turnovers)
            rows_to_insert.append((team, havoc_score, sacks_pg, turnovers_pg))

        # 3. SQL Query (The "Upsert")
        # "ON CONFLICT (team_name) DO UPDATE" means:
        # If the team exists, update their stats. If not, insert them.
        query = """
            INSERT INTO defensive_intel (team_name, havoc_score, sacks_pg, turnovers_pg)
            VALUES %s
            ON CONFLICT (team_name) DO UPDATE 
            SET havoc_score = EXCLUDED.havoc_score,
                sacks_pg = EXCLUDED.sacks_pg,
                turnovers_pg = EXCLUDED.turnovers_pg,
                updated_at = CURRENT_TIMESTAMP;
        """
        
        execute_values(cursor, query, rows_to_insert)
        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"✅ Successfully saved {len(rows_to_insert)} teams to the Database!")
        
    except Exception as e:
        print(f"\n❌ Database Error: {e}")

if __name__ == "__main__":
    # 1. Fetch the stats from the internet
    prefetch_defensive_intel()
    
    # 2. Save them to your new Database table
    update_database()