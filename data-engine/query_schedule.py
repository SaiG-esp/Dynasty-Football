import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }

# Standard default year, but we could make this an input too if you want history
CURRENT_YEAR = 2024 

def search_player(name_query):
    """
    Searches for a player and returns their details (Name, Team, Position).
    """
    print(f"🔍 Searching for '{name_query}'...", end="\r")
    url = "https://api.collegefootballdata.com/player/search"
    params = { "searchTerm": name_query, "year": CURRENT_YEAR }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        results = resp.json()
        
        if not results:
            print(f"❌ No player found named '{name_query}' for {CURRENT_YEAR}.")
            return None

        # If exactly one match, use it
        if len(results) == 1:
            p = results[0]
            print(f"✅ Found: {p['name']} ({p['team']} - {p['position']})")
            return p
            
        # If multiple matches, let user choose
        print(f"\n⚠️ Multiple players found for '{name_query}':")
        for i, p in enumerate(results):
            print(f"   {i+1}. {p['name']} -- {p['team']} ({p['position']})")
            
        choice = input(f"\nEnter the number (1-{len(results)}) of the player you want: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                return results[idx]
        except:
            pass
            
        print("❌ Invalid selection.")
        return None

    except Exception as e:
        print(f"❌ Search Error: {e}")
        return None

def get_schedule_map(team_name):
    """
    Fetches the schedule for the SPECIFIC team to build the date map.
    """
    print(f"📅 Fetching {CURRENT_YEAR} Schedule for {team_name}...", end="\r")
    schedule_map = {}
    url = "https://api.collegefootballdata.com/games"

    for season_type in ['regular', 'postseason']:
        params = { "year": CURRENT_YEAR, "team": team_name, "seasonType": season_type }
        
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
            if resp.status_code == 200:
                games = resp.json()
                for game in games:
                    g_id = str(game.get('id'))
                    
                    # 1. Get Date (Using verified key 'startDate')
                    raw_date = game.get('startDate')
                    fmt_date = "9999-12-31"
                    if raw_date:
                        try:
                            dt = parser.parse(raw_date)
                            fmt_date = dt.strftime("%Y-%m-%d")
                        except: pass

                    # 2. Get Opponent (Using verified keys 'homeTeam' / 'awayTeam')
                    home = game.get('homeTeam')
                    away = game.get('awayTeam')
                    opponent = away if home == team_name else home
                    if opponent is None: opponent = "TBD"
                        
                    schedule_map[g_id] = {
                        "date": fmt_date,
                        "opponent": opponent,
                        "week": game.get('week', 0)
                    }
        except: pass
            
    return schedule_map

def get_player_stats(player_name, team_name):
    # 1. Load Schedule Map for the Player's Team
    game_map = get_schedule_map(team_name)
    if not game_map:
        print(f"❌ Could not load schedule for {team_name}.")
        return

    print(f"\n🏈 --- FETCHING STATS: {player_name.upper()} ({team_name}) ---")
    url = "https://api.collegefootballdata.com/games/players"
    
    all_rows = []

    # 2. Fetch Stats
    for season_type in ['regular', 'postseason']:
        params = {
            "year": CURRENT_YEAR,
            "team": team_name,
            "seasonType": season_type,
            "category": "receiving" # Default to receiving
        }
        
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
            games_data = resp.json()
            
            for game in games_data:
                game_id = str(game.get('id'))
                
                # Match to Schedule Map
                info = game_map.get(game_id)
                if info:
                    r_date = info['date']
                    r_opp = info['opponent']
                    r_wk = info['week']
                else:
                    r_date, r_opp, r_wk = "Unknown", "Unknown", 0
                
                # Find Player Stats within the game object
                found = False
                rec, yds, td = 0, 0, 0
                
                for t in game.get('teams', []):
                    # Check both 'school' (stats endpoint) and 'team' keys
                    if t.get('school') == team_name or t.get('team') == team_name:
                        for cat in t.get('categories', []):
                            if cat.get('name') == 'receiving':
                                for s_type in cat.get('types', []):
                                    s_name = s_type.get('name')
                                    for ath in s_type.get('athletes', []):
                                        if ath.get('name') == player_name:
                                            found = True
                                            try:
                                                v = int(ath.get('stat', 0))
                                                if s_name == 'REC': rec = v
                                                elif s_name == 'YDS': yds = v
                                                elif s_name == 'TD': td = v
                                            except: pass
                
                if found:
                    all_rows.append({
                        "Date": r_date,
                        "Week": r_wk,
                        "Opponent": r_opp,
                        "Rec": rec, "Yds": yds, "TD": td
                    })

        except Exception as e:
            print(f"❌ Error: {e}")

    # 3. Print & Save Results
    if all_rows:
        df = pd.DataFrame(all_rows)
        df = df.sort_values(by=['Date'])
        
        print("\n" + "="*65)
        print(f"{'DATE':<12} {'WK':<4} {'OPPONENT':<22} {'REC':<5} {'YDS':<5} {'TD':<5}")
        print("-" * 65)
        for i, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Week']:<4} {r['Opponent']:<22} {r['Rec']:<5} {r['Yds']:<5} {r['TD']:<5}")
        print("="*65)
        print(f"{'TOTAL':<40} {df['Rec'].sum():<5} {df['Yds'].sum():<5} {df['TD'].sum():<5}")
        
        fname = f"{player_name.replace(' ', '_')}_{CURRENT_YEAR}.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to {fname}")
    else:
        print(f"❌ No receiving stats found for {player_name} in {CURRENT_YEAR}.")

# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        query = input("Enter Player Name (or 'q' to quit): ").strip()
        if query.lower() == 'q':
            break
            
        player_info = search_player(query)
        
        if player_info:
            # We now have the EXACT name and EXACT team from the API
            # This prevents spelling errors from breaking the next step
            get_player_stats(player_info['name'], player_info['team'])