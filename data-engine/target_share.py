import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }
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

def calculate_touch_share(player_data):
    name = player_data['name']
    team = player_data['team']
    pos = player_data['position']
    print(f"📡 Scanning Touch Share for {name}...", end="\r")
    
    # { game_id: { 'team_plays': 0, 'player_touches': 0, 'yards': 0 } }
    usage_stats = {}
    url = "https://api.collegefootballdata.com/plays"
    
    for week in range(1, 16):
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": team, "week": week})
            plays = resp.json()
            
            for play in plays:
                g_id = str(play.get('gameId'))
                if g_id not in usage_stats:
                    usage_stats[g_id] = { "team_plays": 0, "player_touches": 0, "yards": 0 }
                
                # --- FILTER 1: MUST BE OUR TEAM ON OFFENSE ---
                # This fixes the "138 snaps" error. We only want OSU offensive plays.
                if play.get('offense') != team:
                    continue

                # --- FILTER 2: MUST BE A REAL PLAY ---
                # Exclude punts, field goals, timeouts, etc.
                p_type = play.get('playType', '')
                if any(x in p_type for x in ["Punt", "Kickoff", "Field Goal", "Timeout", "End of"]):
                    continue
                    
                usage_stats[g_id]["team_plays"] += 1
                
                # --- 3. COUNT PLAYER TOUCHES ---
                # We assume a player "Touched" the ball if their name is in the text
                if name in play.get('playText', ''):
                    is_touch = False
                    
                    # Skill Players: Rush or Reception
                    if "Rush" in p_type or "Reception" in p_type or "Touchdown" in p_type:
                         is_touch = True
                    
                    # QBs: Pass or Rush (Sacks count as 'Dropbacks' for usage)
                    if pos == 'QB' and ("Pass" in p_type or "Sack" in p_type):
                         is_touch = True
                         
                    if is_touch:
                        usage_stats[g_id]["player_touches"] += 1
                        usage_stats[g_id]["yards"] += play.get('yardsGained', 0)

        except: pass
        
    return usage_stats

def run_analysis():
    p_data = search_player(input("\nEnter Player Name: ").strip())
    if not p_data: return

    game_map = get_schedule_map(p_data['team'])
    stats = calculate_touch_share(p_data)
    
    rows = []
    
    s_plays = 0
    s_touches = 0
    s_yards = 0
    
    sorted_games = sorted(game_map.items(), key=lambda x: x[1]['date'])
    
    for g_id, info in sorted_games:
        data = stats.get(g_id)
        if data and data['team_plays'] > 0:
            
            t_plays = data['team_plays']
            p_touches = data['player_touches']
            p_yards = data['yards']
            
            # THE CALCULATION: Touches / Total Team OFFENSIVE Snaps
            share_pct = (p_touches / t_plays * 100)
            
            s_plays += t_plays
            s_touches += p_touches
            s_yards += p_yards
            
            rows.append({
                "Date": info['date'],
                "Opponent": info['opponent'],
                "Team_Snaps": t_plays,
                "Touches": p_touches,
                "Touch_Share": f"{share_pct:.1f}%",
                "Yards": p_yards
            })

    if rows:
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print(f"📊 TOUCH SHARE REPORT: {p_data['name'].upper()} ({p_data['position']})")
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'SNAPS':<6} {'TOUCH':<6} {'SHARE':<6} {'YDS':<5}")
        print("-" * 80)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Team_Snaps']:<6} {r['Touches']:<6} {r['Touch_Share']:<6} {r['Yards']:<5}")
            
        print("-" * 80)
        
        total_share = (s_touches / s_plays * 100) if s_plays > 0 else 0.0
        print(f"{'TOTAL':<34} | {s_plays:<6} {s_touches:<6} {f'{total_share:.1f}%':<6} {s_yards:<5}")
        print("="*80)
        print("* SNAPS = Total offensive plays (Offense Only)")
        print("* SHARE = % of Team Snaps where Player touched the ball")
        
        fname = f"{p_data['name'].replace(' ', '_')}_touch_share_fixed_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No stats found.")

if __name__ == "__main__":
    run_analysis()