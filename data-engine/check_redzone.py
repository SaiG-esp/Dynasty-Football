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

def analyze_redzone_performance(player_data):
    """ 
    Calculates Team TDs vs FGs separately alongside Player stats.
    """
    name = player_data['name']
    team = player_data['team']
    pos = player_data['position']
    print(f"📡 Scanning PBP for {name} ({pos}) inside the 20...", end="\r")
    
    # Structure: { game_id: { 'team_rz_drives': Set, 'team_td_drives': Set, 'team_fg_drives': Set, ... } }
    game_data = {}
    
    url = "https://api.collegefootballdata.com/plays"
    
    for week in range(1, 16):
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": team, "week": week})
            plays = resp.json()
            
            for play in plays:
                g_id = str(play.get('gameId'))
                drive_id = play.get('driveId')
                
                if g_id not in game_data:
                    game_data[g_id] = { 
                        "team_rz_drives": set(), 
                        "team_td_drives": set(),
                        "team_fg_drives": set(),
                        "p_opps": 0, "p_yards": 0, "p_tds": 0 
                    }
                
                # --- 1. CHECK RED ZONE STATUS ---
                ytg = play.get('yardsToGoal')
                
                if ytg is not None and int(ytg) <= 20:
                    game_data[g_id]["team_rz_drives"].add(drive_id)
                    
                    # --- 2. CHECK SCORING TYPE ---
                    if play.get('scoring') is True:
                        p_type = play.get('playType', '')
                        
                        if "Touchdown" in p_type:
                            game_data[g_id]["team_td_drives"].add(drive_id)
                        elif "Field Goal" in p_type:
                            game_data[g_id]["team_fg_drives"].add(drive_id)

                    # --- 3. PLAYER STATS ---
                    p_text = play.get('playText', '')
                    if name in p_text:
                        p_type = play.get('playType', '')
                        is_valid = False
                        
                        if pos == 'QB':
                            if any(x in p_type for x in ['Pass', 'Rush', 'Sack']): is_valid = True
                        else:
                            if any(x in p_type for x in ['Pass', 'Rush', 'Reception']): is_valid = True
                        
                        if is_valid:
                            game_data[g_id]['p_opps'] += 1
                            game_data[g_id]['p_yards'] += play.get('yardsGained', 0)
                            if "Touchdown" in p_type:
                                game_data[g_id]['p_tds'] += 1
        except: pass
        
    return game_data

def run_analysis():
    p_data = search_player(input("\nEnter Player Name: ").strip())
    if not p_data: return

    game_map = get_schedule_map(p_data['team'])
    combined_stats = analyze_redzone_performance(p_data)
    
    rows = []
    
    # Season Totals
    s_trips = 0
    s_scores = 0 # Total Scores (TD + FG)
    s_team_tds = 0
    s_team_fgs = 0
    
    s_opps = 0
    s_yds = 0
    s_tds = 0
    
    sorted_games = sorted(game_map.items(), key=lambda x: x[1]['date'])
    
    for g_id, info in sorted_games:
        stats = combined_stats.get(g_id)
        
        if stats:
            t_trips = len(stats['team_rz_drives'])
            
            # Intersection logic: Only count scores if they started/happened on an RZ drive
            rz_tds = len(stats['team_td_drives'].intersection(stats['team_rz_drives']))
            rz_fgs = len(stats['team_fg_drives'].intersection(stats['team_rz_drives']))
            rz_total_scores = rz_tds + rz_fgs
            
            p_opps = stats['p_opps']
            
            if t_trips > 0 or p_opps > 0:
                t_pct = (rz_total_scores / t_trips * 100) if t_trips > 0 else 0.0
                
                s_trips += t_trips
                s_scores += rz_total_scores
                s_team_tds += rz_tds
                s_team_fgs += rz_fgs
                
                s_opps += p_opps
                s_yds += stats['p_yards']
                s_tds += stats['p_tds']
                
                rows.append({
                    "Date": info['date'],
                    "Opponent": info['opponent'],
                    "Team_Trips": t_trips,
                    "Team_TDs": rz_tds,  # New Column
                    "Team_FGs": rz_fgs,  # New Column
                    "Team_Conv": f"{t_pct:.0f}%",
                    "Pl_Opps": p_opps,
                    "Pl_Yds": stats['p_yards'],
                    "Pl_TDs": stats['p_tds']
                })

    if rows:
        df = pd.DataFrame(rows)
        print("\n" + "="*95)
        print(f"🚨 RED ZONE REPORT: {p_data['name'].upper()} ({p_data['position']})")
        # Adjusted formatting for new columns
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'TRIPS':<5} {'TDS':<3} {'FGS':<3} {'CONV %':<6} | {'PL OPPS':<8} {'YDS':<5} {'TDS':<5}")
        print("-" * 95)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Team_Trips']:<5} {r['Team_TDs']:<3} {r['Team_FGs']:<3} {r['Team_Conv']:<6} | {r['Pl_Opps']:<8} {r['Pl_Yds']:<5} {r['Pl_TDs']:<5}")
        
        print("-" * 95)
        
        total_pct = (s_scores / s_trips * 100) if s_trips > 0 else 0.0
        print(f"{'TOTAL':<34} | {s_trips:<5} {s_team_tds:<3} {s_team_fgs:<3} {f'{total_pct:.0f}%':<6} | {s_opps:<8} {s_yds:<5} {s_tds:<5}")
        print("="*95)
        
        fname = f"{p_data['name'].replace(' ', '_')}_redzone_detailed_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No stats found.")

if __name__ == "__main__":
    run_analysis()