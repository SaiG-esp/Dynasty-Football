import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }
YEAR = 2024

# --- CACHE FOR DEFENSIVE STATS ---
OPPONENT_INTEL = {}

def search_team():
    q = input("\nEnter Team Name (e.g. Arizona State): ").strip()
    print(f"🔍 Searching for '{q}'...", end="\r")
    url = "https://api.collegefootballdata.com/teams"
    try:
        resp = requests.get(url, headers=HEADERS)
        teams = resp.json()
        matches = [t for t in teams if q.lower() in t['school'].lower()]
        if not matches: return None
        if len(matches) == 1: return matches[0]['school']
        print(f"\n⚠️ Multiple teams found:")
        for i, t in enumerate(matches[:5]):
            print(f"   {i+1}. {t['school']}")
        choice = input(f"Select # (1-{len(matches[:5])}): ")
        return matches[int(choice)-1]['school']
    except: return None

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
                    'tfl': 0, 
                    'sacks': 0, 
                    'int': 0, 
                    'pd': 0, 
                    'fumbles': 0, 
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

    print("✅ Defensive Intel Loaded.                 ")

def get_havoc_rating(opponent):
    """
    Returns: Weighted Havoc, Sacks PG, Turnovers PG
    Formula: (TFL + 2*Int + 2*Fum + 1.5*Sacks + PD) / Games
    """
    if opponent not in OPPONENT_INTEL:
        return 0, 0, 0
    
    s = OPPONENT_INTEL[opponent]
    g = s['games']
    
    # Raw Totals
    tfl = s['tfl']
    ints = s['int']
    fums = s['fumbles']
    sacks = s['sacks']
    pd = s['pd']
    
    # 1. Calculate Weighted Havoc Score
    # Formula: TFL + 2(Int) + 2(Fumbles) + 1.5(Sacks) + PD
    weighted_sum = tfl + (2 * ints) + (2 * fums) + (1.5 * sacks) + pd
    havoc_score = weighted_sum / g
    
    # 2. Calculate Specific Averages
    sacks_pg = sacks / g
    turnovers_pg = (ints + fums) / g
    
    return havoc_score, sacks_pg, turnovers_pg

def calculate_relative_rating(spread, avg_spread):
    deviation = spread - avg_spread
    raw_rating = 5.5 + (deviation / 6.0)
    rating = int(round(max(1, min(10, raw_rating))))
    return rating

def get_matchup_data(team_name):
    print(f"📡 Analyzing schedule for {team_name}...", end="\r")
    url = "https://api.collegefootballdata.com/lines"
    params = { "year": YEAR, "team": team_name }
    
    rows = []
    spreads = []
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        games = resp.json()
        
        game_data_list = []
        
        for game in games:
            lines = game.get('lines', [])
            if not lines: continue
            
            selected_line = lines[0] 
            providers = {line.get('provider'): line for line in lines}
            if 'consensus' in providers: selected_line = providers['consensus']
            elif 'DraftKings' in providers: selected_line = providers['DraftKings']
            
            spread = selected_line.get('spread')
            if spread is None: continue
            
            home = game.get('homeTeam')
            away = game.get('awayTeam')
            opponent = away if home == team_name else home
            
            formatted = selected_line.get('formattedSpread', '')
            my_spread = 0.0
            
            if team_name in formatted:
                try:
                    val_str = formatted.split(team_name)[1].strip().split(' ')[0]
                    my_spread = float(val_str)
                except: my_spread = float(spread)
            else:
                try:
                    val_str = formatted.split(opponent)[1].strip().split(' ')[0]
                    my_spread = -1 * float(val_str)
                except: my_spread = float(spread)
                
            spreads.append(my_spread)
            
            game_data_list.append({
                "game": game, 
                "my_spread": my_spread, 
                "opponent": opponent
            })
            
        if not spreads: return [], 0
        
        avg_spread = sum(spreads) / len(spreads)
        
        for item in game_data_list:
            g = item['game']
            opponent = item['opponent']
            my_spread = item['my_spread']
            
            rating = calculate_relative_rating(my_spread, avg_spread)
            
            havoc_score, sacks_pg, turnovers_pg = get_havoc_rating(opponent)
            
            raw_date = g.get('startDate')
            fmt_date = parser.parse(raw_date).strftime("%Y-%m-%d") if raw_date else "TBD"
            
            rows.append({
                "Date": fmt_date,
                "Opponent": opponent,
                "Spread": my_spread,
                "Rating": rating,
                "Havoc_Score": havoc_score,
                "Sacks_PG": sacks_pg,
                "TO_PG": turnovers_pg
            })
            
    except Exception as e:
        print(f"Error: {e}")
        pass
    
    return rows, avg_spread if spreads else 0

def run_analysis():
    prefetch_defensive_intel()
    team = search_team()
    if not team: return

    data, avg_spread = get_matchup_data(team)
    
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by='Date')
        
        print("\n" + "="*100)
        print(f"⚔️  MATCHUP ANALYZER: {team.upper()}")
        # Explicitly printing the baseline spread
        print(f"   Baseline Spread: {avg_spread:+.1f} (Average line for {team})")
        print(f"   Havoc Formula: (TFL + 2*Int + 2*Fum + 1.5*Sacks + PD) / Games")
        print("-" * 100)
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'LINE':<6} | {'RTG':<3} | {'HAVOC':<6} | {'SACK/G':<6} | {'TO/G':<5} | {'ANALYSIS'}")
        print("-" * 100)
        
        for _, r in df.iterrows():
            rating = r['Rating']
            havoc = r['Havoc_Score']
            sacks = r['Sacks_PG']
            tos = r['TO_PG']
            
            h_str = f"{havoc:.1f}"
            s_str = f"{sacks:.1f}"
            t_str = f"{tos:.1f}"
            
            # Simplified Description Logic
            desc = "Average"
            if rating >= 8: desc = "BRUTAL"
            elif rating >= 6: desc = "Tough"
            elif rating <= 3: desc = "Easy Win"
            
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {r['Spread']:<+6.1f} | {rating:<3} | {h_str:<6} | {s_str:<6} | {t_str:<5} | {desc}")
            
        print("="*100)
        
        fname = f"{team.replace(' ', '_')}_matchup_intel_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Intelligence saved to '{fname}'")
    else:
        print("\n❌ No data found.")

if __name__ == "__main__":
    run_analysis()