import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
from config import API_KEY, HEADERS
YEAR = 2024

def search_team():
    q = input("\nEnter Team Name (e.g. Ohio State): ").strip()
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

def get_betting_data(team_name):
    print(f"📡 Fetching Betting Lines for {team_name}...", end="\r")
    url = "https://api.collegefootballdata.com/lines"
    params = { "year": YEAR, "team": team_name }
    
    rows = []
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        games = resp.json()
        
        for game in games:
            # 1. Basic Info
            g_id = str(game.get('id'))
            home = game.get('homeTeam')
            away = game.get('awayTeam')
            opponent = away if home == team_name else home
            
            # 2. Find the Line (Smart Selector)
            lines = game.get('lines', [])
            if not lines: continue
            
            # Priority: Consensus -> DraftKings -> Bovada -> First Available
            selected_line = lines[0] 
            providers = {line.get('provider'): line for line in lines}
            
            if 'consensus' in providers: selected_line = providers['consensus']
            elif 'DraftKings' in providers: selected_line = providers['DraftKings']
            elif 'Bovada' in providers: selected_line = providers['Bovada']
            
            spread = selected_line.get('spread')
            over_under = selected_line.get('overUnder')
            provider_name = selected_line.get('provider')
            
            if spread is None or over_under is None: continue
            
            fmt_spread = selected_line.get('formattedSpread', '')
            
            # 3. Calculate Spread relative to US
            # If "Ohio State -50.5", my_spread is -50.5
            my_spread = 0.0
            if team_name in fmt_spread:
                try:
                    parts = fmt_spread.split(team_name)
                    val_str = parts[1].strip().split(' ')[0]
                    my_spread = float(val_str)
                except: my_spread = float(spread)
            else:
                # If "Akron +50.5", then Ohio State is -50.5
                try:
                    parts = fmt_spread.split(opponent)
                    val_str = parts[1].strip().split(' ')[0]
                    opp_spread = float(val_str)
                    my_spread = -1 * opp_spread
                except: my_spread = float(spread)

            # 4. Implied Total Formula
            implied_points = (float(over_under) - my_spread) / 2
            
            # Parse Date
            raw_date = game.get('startDate')
            fmt_date = "9999-12-31"
            if raw_date:
                try: fmt_date = parser.parse(raw_date).strftime("%Y-%m-%d")
                except: pass
                
            rows.append({
                "Date": fmt_date,
                "Opponent": opponent,
                "Provider": provider_name,
                "Spread": fmt_spread,
                "Total": over_under,
                "Implied_Pts": implied_points
            })
            
    except: pass
    
    return rows

def run_analysis():
    team = search_team()
    if not team: return

    data = get_betting_data(team)
    
    if data:
        df = pd.DataFrame(data)
        # Sort Chronologically
        df = df.sort_values(by='Date')
        
        print("\n" + "="*95)
        print(f"🎰 BETTING TIMELINE: {team.upper()}")
        print(f"{'DATE':<12} {'OPPONENT':<18} | {'LINE':<20} {'O/U':<6} | {'IMPLIED PTS':<12}")
        print("-" * 95)
        
        for _, r in df.iterrows():
            print(f"{r['Date']:<12} {r['Opponent']:<18} | {r['Spread']:<20} {r['Total']:<6} | {r['Implied_Pts']:.1f}")
            
        print("="*95)
        print("* IMPLIED PTS: What Vegas expected the team to score.")
        
        fname = f"{team.replace(' ', '_')}_betting_timeline_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No betting data found.")

if __name__ == "__main__":
    run_analysis()