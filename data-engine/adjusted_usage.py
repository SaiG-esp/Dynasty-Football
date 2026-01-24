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

def calculate_adjusted_usage(player_data):
    name = player_data['name']
    team = player_data['team']
    pos = player_data['position']
    print(f"📡 Scanning Adjusted Usage (Excluding Obvious Runs)...", end="\r")
    
    usage_stats = {}
    url = "https://api.collegefootballdata.com/plays"
    
    for week in range(1, 16):
        try:
            resp = requests.get(url, headers=HEADERS, params={"year": YEAR, "team": team, "week": week})
            plays = resp.json()
            
            for play in plays:
                # 1. Team & Play Type Filter
                if play.get('offense') != team: continue
                p_type = play.get('playType', '')
                if any(x in p_type for x in ["Punt", "Kickoff", "Field Goal", "Timeout", "End of"]): continue

                # 2. CONTEXT FILTER: Is this an Obvious Run?
                down = play.get('down')
                dist = play.get('distance')
                
                is_obvious_run = False
                if down is not None and dist is not None:
                     # Definition: 1st/2nd & <5 OR 3rd & <=3
                     if (down in [1, 2] and dist < 5) or (down == 3 and dist <= 3):
                         is_obvious_run = True
                
                # IF OBVIOUS RUN, SKIP THIS PLAY (It's not a relevant sample)
                if is_obvious_run:
                    continue

                # 3. Process the "Relevant" Play
                g_id = str(play.get('gameId'))
                if g_id not in usage_stats:
                    usage_stats[g_id] = { "adj_snaps": 0, "adj_touches": 0, "adj_yards": 0 }
                
                usage_stats[g_id]["adj_snaps"] += 1
                
                # 4. Check for Player Touch
                if name in play.get('playText', ''):
                    is_touch = False
                    if "Rush" in p_type or "Reception" in p_type or "Touchdown" in p_type: is_touch = True
                    if pos == 'QB' and ("Pass" in p_type or "Sack" in p_type): is_touch = True
                         
                    if is_touch:
                        usage_stats[g_id]["adj_touches"] += 1
                        usage_stats[g_id]["adj_yards"] += play.get('yardsGained', 0)

        except: pass
        
    return usage_stats

def run_analysis():
    p_data = search_player(input("\nEnter Player Name: ").strip())
    if not p_data: return

    game_map = get_schedule_map(p_data['team'])
    stats = calculate_adjusted_usage(p_data)
    
    rows = []
    sorted_games = sorted(game_map.items(), key=lambda x: x[1]['date'])
    
    for g_id, info in sorted_games:
        data = stats.get(g_id)
        if data and data['adj_snaps'] > 0:
            
            t_snaps = data['adj_snaps']
            p_touches = data['adj_touches']
            share_pct = (p_touches / t_snaps * 100)
            
            rows.append({
                "Date": info['date'],
                "Opponent": info['opponent'],
                "Adj_Snaps": t_snaps,
                "Adj_Touch": p_touches,
                "Adj_Share": f"{share_pct:.1f}%",
                "Adj_Yds": data['adj_yards']
            })

    if rows:
        df = pd.DataFrame(rows)
        print("\n" + "="*85)
        print(f"🎯 SITUATIONAL USAGE: {p_data['name'].upper()} (Excl. Obvious Runs)")
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'SNAPS*':<6} {'TOUCH':<6} {'SHARE %':<8} {'YDS':<5}")
        print("-" * 85)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Adj_Snaps']:<6} {r['Adj_Touch']:<6} {r['Adj_Share']:<8} {r['Adj_Yds']:<5}")
            
        print("-" * 85)
        print("* SNAPS = Only plays where Down/Dist allowed a realistic pass/run option.")
        print("  (Excluded: 1st/2nd & <5, 3rd & <=3)")
        
        fname = f"{p_data['name'].replace(' ', '_')}_situational_usage_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No stats found.")

if __name__ == "__main__":
    run_analysis()