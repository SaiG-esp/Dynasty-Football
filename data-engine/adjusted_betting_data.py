import requests
import pandas as pd
import warnings
import numpy as np
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
from config import API_KEY, HEADERS
YEAR = 2024

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

def calculate_relative_rating(spread, avg_spread):
    """
    Calculates 1-10 rating based on deviation from the team's average.
    Higher Spread (e.g. +7 vs -10) = Harder Game.
    Step size approx 6 points per rating point.
    """
    deviation = spread - avg_spread
    
    # Base is 5.5 (Average Game)
    raw_rating = 5.5 + (deviation / 6.0)
    
    # Clamp between 1 and 10
    rating = int(round(max(1, min(10, raw_rating))))
    return rating

def get_betting_data(team_name):
    print(f"📡 Calculating Relative Difficulty for {team_name}...", end="\r")
    url = "https://api.collegefootballdata.com/lines"
    params = { "year": YEAR, "team": team_name }
    
    rows = []
    spreads = []
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        games = resp.json()
        
        # FIRST PASS: Collect all spreads for Baseline
        game_data_list = []
        
        for game in games:
            lines = game.get('lines', [])
            if not lines: continue
            
            # Smart Selector
            selected_line = lines[0] 
            providers = {line.get('provider'): line for line in lines}
            
            if 'consensus' in providers: selected_line = providers['consensus']
            elif 'DraftKings' in providers: selected_line = providers['DraftKings']
            elif 'Bovada' in providers: selected_line = providers['Bovada']
            
            spread = selected_line.get('spread')
            if spread is None: continue
            
            # Calculate 'My Spread'
            formatted = selected_line.get('formattedSpread', '')
            my_spread = 0.0
            
            home = game.get('homeTeam')
            away = game.get('awayTeam')
            opponent = away if home == team_name else home
            
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
                "opponent": opponent,
                "formatted": formatted
            })
            
        if not spreads: return []
        
        # BASELINE CALCULATION
        avg_spread = sum(spreads) / len(spreads)
        
        # SECOND PASS: Assign Ratings
        for item in game_data_list:
            g = item['game']
            my_spread = item['my_spread']
            
            rating = calculate_relative_rating(my_spread, avg_spread)
            
            raw_date = g.get('startDate')
            fmt_date = "9999-12-31"
            if raw_date:
                try: fmt_date = parser.parse(raw_date).strftime("%Y-%m-%d")
                except: pass
            
            rows.append({
                "Date": fmt_date,
                "Opponent": item['opponent'],
                "Spread": my_spread,
                "Rating": rating,
                "Formatted": item['formatted']
            })
            
    except: pass
    
    return rows, avg_spread if spreads else 0

def run_analysis():
    team = search_team()
    if not team: return

    data, avg_spread = get_betting_data(team)
    
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by='Date')
        
        print("\n" + "="*95)
        print(f"📊 RELATIVE DIFFICULTY REPORT: {team.upper()}")
        print(f"   Team Baseline Spread: {avg_spread:+.1f} (Average Game)")
        print("-" * 95)
        print(f"{'DATE':<12} {'OPPONENT':<20} | {'SPREAD':<6} | {'RATING':<8} | {'CATEGORY'}")
        print("-" * 95)
        
        for _, r in df.iterrows():
            rating = r['Rating']
            spread_val = r['Spread']
            
            # Visual Bar
            bar = "█" * rating
            
            # --- NEW DESCRIPTORS ---
            desc = ""
            if rating <= 3: 
                desc = "Easy Win"
            elif rating <= 6: 
                desc = "Average Game"
            elif rating <= 8: 
                desc = "Challenge"
            else: 
                desc = "BRUTAL GAME"
            
            print(f"{r['Date']:<12} {r['Opponent']:<20} | {spread_val:<+6.1f} | {rating:<8} | {bar:<10} {desc}")
            
        print("="*95)
        
        fname = f"{team.replace(' ', '_')}_relative_difficulty_2024.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print("\n❌ No betting data found.")

if __name__ == "__main__":
    run_analysis()