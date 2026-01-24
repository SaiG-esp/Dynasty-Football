import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }

TARGET_PLAYER = "Will Howard"
TARGET_TEAM = "Ohio State"
YEAR = 2024

def get_official_team_stats():
    """
    Fetches the OFFICIAL box score stats (pre-calculated by the NCAA).
    """
    print(f"📊 Fetching Official Team Stats...", end="\r")
    official_data = {}
    
    url = "https://api.collegefootballdata.com/games/teams"
    params = { "year": YEAR, "team": TARGET_TEAM }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        games = resp.json()
        
        for game in games:
            g_id = str(game.get('id'))
            
            # Find the Ohio State object in this game
            for team in game.get('teams', []):
                # --- ROBUST KEY CHECK ---
                # Check all possible keys for the school name
                t_name = team.get('school') or team.get('team') or team.get('schoolName')
                
                if t_name == TARGET_TEAM:
                    # Loop through stats to find "3rd Down Efficiency"
                    for stat in team.get('stats', []):
                        if stat.get('category') == 'thirdDownEff':
                            # Format is usually "5-15" (Made-Att)
                            val = stat.get('stat')
                            try:
                                made, att = map(int, val.split('-'))
                                official_data[g_id] = { "team_att": att, "team_conv": made }
                            except:
                                pass
    except Exception as e:
        print(f"\n⚠️ Team Stats Error: {e}")
        
    return official_data

def get_schedule_map():
    schedule_map = {}
    url = "https://api.collegefootballdata.com/games"
    for season_type in ['regular', 'postseason']:
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": TARGET_TEAM, "seasonType": season_type})
            for game in resp.json():
                g_id = str(game.get('id'))
                # Parse Date
                raw_date = game.get('startDate')
                fmt_date = "9999-12-31"
                if raw_date:
                    try:
                        fmt_date = parser.parse(raw_date).strftime("%Y-%m-%d")
                    except: pass
                # Parse Opponent
                home, away = game.get('homeTeam'), game.get('awayTeam')
                opponent = away if home == TARGET_TEAM else home
                if opponent is None: opponent = "TBD"
                
                schedule_map[g_id] = { "date": fmt_date, "opponent": opponent, "week": game.get('week', 0) }
        except: pass
    return schedule_map

def run_analysis():
    # 1. Get Official Data (The Answer Key)
    team_stats = get_official_team_stats()
    game_map = get_schedule_map()
    print(f"✅ Loaded Official Stats for {len(team_stats)} games.")
    
    # 2. Get Will Howard Data (The Student Work)
    print(f"📡 Scanning Play-by-Play for {TARGET_PLAYER}...", end="\r")
    player_stats = {}
    
    url = "https://api.collegefootballdata.com/plays"
    for week in range(1, 16):
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": TARGET_TEAM, "week": week})
            plays = resp.json()
            
            for play in plays:
                # Filter: 3rd Down & Pass Only
                if play.get('down') != 3: continue
                
                p_type = play.get('playType', '')
                # Exclude Sacks (NCAA counts them as rushing)
                if 'Pass' not in p_type and 'Interception' not in p_type: continue
                
                # Filter: Will Howard (using camelCase 'playText')
                if TARGET_PLAYER not in play.get('playText', ''): continue
                
                g_id = str(play.get('gameId'))
                if g_id not in player_stats:
                    player_stats[g_id] = { "att": 0, "comp": 0 }
                
                player_stats[g_id]['att'] += 1
                
                # Completion Logic
                is_comp = False
                if "Reception" in p_type: is_comp = True
                elif "Touchdown" in p_type and "Interception" not in p_type: is_comp = True
                
                if is_comp: player_stats[g_id]['comp'] += 1
        except: pass

    # 3. Merge & Display
    final_rows = []
    
    # We loop through the OFFICIAL games to ensure we don't miss anything
    for g_id, official in team_stats.items():
        info = game_map.get(g_id, {'date': 'Unknown', 'opponent': 'Unknown', 'week': 0})
        
        # Team Official Stats
        t_att = official['team_att']
        t_conv = official['team_conv']
        t_pct = (t_conv / t_att * 100) if t_att > 0 else 0.0
        
        # Player Stats (calculated)
        p_data = player_stats.get(g_id, {'att': 0, 'comp': 0})
        p_att = p_data['att']
        p_comp = p_data['comp']
        p_pct = (p_comp / p_att * 100) if p_att > 0 else 0.0
        
        final_rows.append({
            "Date": info['date'],
            "Opponent": info['opponent'],
            "Team_Att": t_att,
            "Team_Conv": t_conv,
            "Team_Pct": f"{t_pct:.0f}%",
            "WH_Att": p_att,
            "WH_Comp": p_comp,
            "WH_Pct": f"{p_pct:.0f}%"
        })
        
    # Sort and Print
    if final_rows:
        df = pd.DataFrame(final_rows).sort_values(by='Date')
        
        print("\n" + "="*90)
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'TEAM (OFFICIAL)':<18} | {'WILL HOWARD (PBP)':<18}")
        print(f"{'':<34} | {'ATT':<4} {'CNV':<4} {'%':<5}    | {'ATT':<4} {'CMP':<4} {'%':<5}")
        print("-" * 90)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Team_Att']:<4} {r['Team_Conv']:<4} {r['Team_Pct']:<5}    | {r['WH_Att']:<4} {r['WH_Comp']:<4} {r['WH_Pct']:<5}")
            
        print("="*90)
        fname = "verified_3rd_downs_final.csv"
        df.to_csv(fname, index=False)
        print(f"\n✅ Verification Complete. Saved to '{fname}'")

if __name__ == "__main__":
    run_analysis()