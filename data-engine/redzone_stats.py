import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
from config import API_KEY, HEADERS
YEAR = 2024

def search_player(name_query):
    print(f"🔍 Searching for '{name_query}'...", end="\r")
    url = "https://api.collegefootballdata.com/player/search"
    params = { "searchTerm": name_query, "year": YEAR }
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        results = resp.json()
        if not results:
            print(f"❌ No player found named '{name_query}'.")
            return None
        if len(results) == 1: return results[0]
        
        print(f"\n⚠️ Multiple players found:")
        for i, p in enumerate(results):
            print(f"   {i+1}. {p['name']} -- {p['team']} ({p['position']})")
        choice = input(f"Select # (1-{len(results)}): ")
        return results[int(choice) - 1]
    except: return None

def get_schedule_map(team_name):
    """ Maps Game IDs to Dates/Opponents """
    schedule_map = {}
    url = "https://api.collegefootballdata.com/games"
    for season_type in ['regular', 'postseason']:
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": team_name, "seasonType": season_type})
            for game in resp.json():
                g_id = str(game.get('id'))
                raw_date = game.get('startDate')
                fmt_date = "9999-12-31"
                if raw_date:
                    try: fmt_date = parser.parse(raw_date).strftime("%Y-%m-%d")
                    except: pass
                
                home, away = game.get('homeTeam'), game.get('awayTeam')
                opp = away if home == team_name else home
                schedule_map[g_id] = { "date": fmt_date, "opponent": opp or "TBD" }
        except: pass
    return schedule_map

def get_team_redzone_stats(team_name):
    """ 
    Fetches OFFICIAL Team Red Zone Stats (Trips & Scores).
    """
    print(f"📊 Fetching Official Red Zone Stats for {team_name}...", end="\r")
    rz_stats = {}
    url = "https://api.collegefootballdata.com/games/teams"
    params = { "year": YEAR, "team": team_name }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        for game in resp.json():
            g_id = str(game.get('id'))
            
            for team in game.get('teams', []):
                # Robust Name Check (Matches 3rd Down Script Logic)
                t_name = team.get('school') or team.get('team') or team.get('schoolName')
                
                if t_name == team_name:
                    trips, scores = 0, 0
                    for stat in team.get('stats', []):
                        cat = stat.get('category')
                        val = int(stat.get('stat', 0))
                        
                        if cat == 'redzoneAttempts': trips = val
                        elif cat == 'redzoneScores': scores = val
                    
                    if trips > 0:
                        rz_stats[g_id] = { "trips": trips, "scores": scores }
    except: pass
    return rz_stats

def analyze_player_redzone(player_data):
    """ Scans PBP for Player usage inside the 20 """
    name = player_data['name']
    team = player_data['team']
    pos = player_data['position']
    print(f"📡 Scanning PBP for {name} ({pos}) inside the 20...", end="\r")
    
    player_rz = {}
    url = "https://api.collegefootballdata.com/plays"
    
    for week in range(1, 16):
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": team, "week": week})
            for play in resp.json():
                # --- FILTER 1: RED ZONE ONLY ---
                # Validated via X-Ray: key is 'yardsToGoal'
                ytg = play.get('yardsToGoal')
                if ytg is None or int(ytg) > 20: continue
                
                # --- FILTER 2: INVOLVES PLAYER ---
                p_text = play.get('playText', '')
                if name not in p_text: continue
                
                g_id = str(play.get('gameId'))
                if g_id not in player_rz: 
                    player_rz[g_id] = { "opps": 0, "yards": 0, "tds": 0 }
                
                # --- FILTER 3: COUNT STATS ---
                p_type = play.get('playType', '')
                
                # Check for Valid Play Types
                is_valid = False
                if pos == 'QB':
                    if any(x in p_type for x in ['Pass', 'Rush', 'Sack']): is_valid = True
                else:
                    if any(x in p_type for x in ['Pass', 'Rush', 'Reception']): is_valid = True
                
                if is_valid:
                    player_rz[g_id]['opps'] += 1
                    player_rz[g_id]['yards'] += play.get('yardsGained', 0)
                    
                    if "Touchdown" in p_type:
                        player_rz[g_id]['tds'] += 1
        except: pass
        
    return player_rz

def run_analysis():
    p_data = search_player(input("\nEnter Player Name: ").strip())
    if not p_data: return

    # 1. Get All Data Sources independently
    game_map = get_schedule_map(p_data['team'])
    team_stats = get_team_redzone_stats(p_data['team'])
    player_stats = analyze_player_redzone(p_data)
    
    # 2. Merge Data based on SCHEDULE (The Safety Net)
    # We loop through the schedule so we never miss a game
    rows = []
    
    season_trips = 0
    season_scores = 0
    season_opps = 0
    season_yds = 0
    season_tds = 0
    
    # Convert map to list of tuples for sorting
    sorted_games = sorted(game_map.items(), key=lambda x: x[1]['date'])
    
    for g_id, info in sorted_games:
        # Check if we have ANY data for this game (Team OR Player)
        t_stat = team_stats.get(g_id, {'trips': 0, 'scores': 0})
        p_stat = player_stats.get(g_id, {'opps': 0, 'yards': 0, 'tds': 0})
        
        # Only print row if something happened (Team Trip OR Player Play)
        if t_stat['trips'] > 0 or p_stat['opps'] > 0:
            
            # Team Stats
            t_trips = t_stat['trips']
            t_scores = t_stat['scores']
            t_pct = (t_scores / t_trips * 100) if t_trips > 0 else 0.0
            
            # Update Season Totals
            season_trips += t_trips
            season_scores += t_scores
            season_opps += p_stat['opps']
            season_yds += p_stat['yards']
            season_tds += p_stat['tds']
            
            rows.append({
                "Date": info['date'],
                "Opponent": info['opponent'],
                "Team_Trips": t_trips,
                "Team_Conv": f"{t_pct:.0f}%",
                "Pl_Opps": p_stat['opps'],
                "Pl_Yds": p_stat['yards'],
                "Pl_TDs": p_stat['tds']
            })

    if rows:
        df = pd.DataFrame(rows)
        print("\n" + "="*85)
        print(f"🚨 RED ZONE REPORT: {p_data['name'].upper()} ({p_data['position']})")
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'TEAM RZ':<8} {'CONV %':<8} | {'PL OPPS':<8} {'YDS':<5} {'TDS':<5}")
        print("-" * 85)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Team_Trips']:<8} {r['Team_Conv']:<8} | {r['Pl_Opps']:<8} {r['Pl_Yds']:<5} {r['Pl_TDs']:<5}")
        
        print("-" * 85)
        
        # Calculate Total Percentage
        total_pct = (season_scores / season_trips * 100) if season_trips > 0 else 0.0
        
        print(f"{'TOTAL':<34} | {season_trips:<8} {f'{total_pct:.0f}%':<8} | {season_opps:<8} {season_yds:<5} {season_tds:<5}")
        print("="*85)
        
        fname = f"{p_data['name'].replace(' ', '_')}_redzone_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No stats found (Checked both Team and Player data).")

if __name__ == "__main__":
    run_analysis()