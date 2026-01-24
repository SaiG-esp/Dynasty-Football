import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
# Suppress SSL warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
PLAYER_TARGET = "Jeremiah Smith"
TEAM_TARGET = "Ohio State"
YEAR = 2024
HEADERS = { "Authorization": f"Bearer {API_KEY}" }

def get_schedule_map():
    """
    Builds a dictionary: { GAME_ID_STRING : { 'date': '2024-08-31', 'opponent': 'Akron' } }
    """
    print(f"📅 Fetching {YEAR} Schedule...", end="\r")
    schedule_map = {}
    url = "https://api.collegefootballdata.com/games"

    for season_type in ['regular', 'postseason']:
        params = { "year": YEAR, "team": TEAM_TARGET, "seasonType": season_type }
        
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                games = resp.json()
                for game in games:
                    # 1. FORCE ID TO STRING
                    g_id = str(game.get('id'))
                    
                    # 2. GET DATE (Using correct key 'startDate')
                    raw_date = game.get('startDate') # Corrected Key
                    if raw_date:
                        try:
                            dt = parser.parse(raw_date)
                            fmt_date = dt.strftime("%Y-%m-%d")
                        except:
                            fmt_date = "9999-12-31"
                    else:
                        fmt_date = "9999-12-31"

                    # 3. GET OPPONENT (Using correct keys 'homeTeam'/'awayTeam')
                    home = game.get('homeTeam')
                    away = game.get('awayTeam')
                    
                    if home == TEAM_TARGET:
                        opponent = away
                    else:
                        opponent = home
                        
                    # Handle NULL opponents in postseason brackets
                    if opponent is None:
                        opponent = "TBD"
                        
                    schedule_map[g_id] = {
                        "date": fmt_date,
                        "opponent": opponent,
                        "week": game.get('week', 0)
                    }
        except Exception:
            pass
            
    return schedule_map

def get_player_stats():
    # 1. BUILD THE MAP FIRST
    game_map = get_schedule_map()
    print(f"✅ Schedule Loaded. Mapped {len(game_map)} games.")

    print(f"\n🏈 --- {YEAR} STATS: {PLAYER_TARGET.upper()} ---")
    url = "https://api.collegefootballdata.com/games/players"
    
    all_game_rows = []

    # 2. FETCH STATS
    for season_type in ['regular', 'postseason']:
        print(f"📡 Fetching {season_type.title()} Stats...", end="\r")
        
        params = {
            "year": YEAR,
            "team": TEAM_TARGET,
            "seasonType": season_type,
            "category": "receiving"
        }
        
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code != 200:
                continue

            games_data = response.json()

            for game in games_data:
                # 3. LINK STATS TO SCHEDULE
                game_id = str(game.get('id'))
                
                # Look up the clean info from our map
                game_info = game_map.get(game_id)
                
                # If map lookup fails, fallback to basic data
                if game_info:
                    real_date = game_info['date']
                    real_opponent = game_info['opponent']
                    real_week = game_info['week']
                else:
                    real_date = "Unknown"
                    real_opponent = "Unknown"
                    real_week = game.get('week', 0)

                # 4. PARSE PLAYER STATS
                rec, yds, td = 0, 0, 0
                player_found = False
                
                teams_box = game.get('teams', [])
                for t in teams_box:
                    # Note: Stats endpoint uses 'school', Schedule uses 'homeTeam'.
                    # We only need this loop to find the PLAYER, not the opponent name anymore.
                    if t.get('school') == TEAM_TARGET or t.get('team') == TEAM_TARGET:
                        for cat in t.get('categories', []):
                            if cat.get('name') == 'receiving':
                                for s_type in cat.get('types', []):
                                    s_name = s_type.get('name')
                                    for ath in s_type.get('athletes', []):
                                        if ath.get('name') == PLAYER_TARGET:
                                            player_found = True
                                            try:
                                                v = int(ath.get('stat', 0))
                                                if s_name == 'REC': rec = v
                                                elif s_name == 'YDS': yds = v
                                                elif s_name == 'TD': td = v
                                            except: pass

                if player_found:
                    all_game_rows.append({
                        "Date": real_date,
                        "Week": real_week,
                        "Opponent": real_opponent,
                        "Rec": rec,
                        "Yds": yds,
                        "TD": td
                    })

        except Exception as e:
            print(f"❌ Stats Error: {e}")

    # 5. FINAL OUTPUT
    if all_game_rows:
        df = pd.DataFrame(all_game_rows)
        
        # Sort Chronologically by Date
        df = df.sort_values(by=['Date'])

        print("\n" + "="*65)
        print(f"{'DATE':<12} {'WK':<4} {'OPPONENT':<22} {'REC':<5} {'YDS':<5} {'TD':<5}")
        print("-" * 65)
        
        for i, row in df.iterrows():
            print(f"{row['Date']:<12} {row['Week']:<4} {row['Opponent']:<22} {row['Rec']:<5} {row['Yds']:<5} {row['TD']:<5}")

        print("-" * 65)
        print(f"{'TOTAL':<40} {df['Rec'].sum():<5} {df['Yds'].sum():<5} {df['TD'].sum():<5}")
        print("="*65)
        
        # Save to CSV
        filename = "jeremiah_smith_2024_complete.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ Success! Data saved to '{filename}'")
        
    else:
        print("\n❌ No stats found.")

if __name__ == "__main__":
    get_player_stats()