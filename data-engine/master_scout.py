import requests
import pandas as pd
import warnings
from dateutil import parser

# 1. SETUP
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
API_KEY = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
HEADERS = { "Authorization": f"Bearer {API_KEY}" }
CURRENT_YEAR = 2024

def search_player(name_query):
    """
    Finds player and identifies their POSITION (QB, RB, WR, etc).
    """
    print(f"🔍 Searching for '{name_query}'...", end="\r")
    url = "https://api.collegefootballdata.com/player/search"
    params = { "searchTerm": name_query, "year": CURRENT_YEAR }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        results = resp.json()
        
        if not results:
            print(f"❌ No player found named '{name_query}'.")
            return None

        # Auto-select if only 1 result
        if len(results) == 1:
            p = results[0]
            print(f"✅ Found: {p['name']} ({p['team']} - {p['position']})")
            return p
            
        # User Selection for multiple matches
        print(f"\n⚠️ Multiple players found:")
        for i, p in enumerate(results):
            print(f"   {i+1}. {p['name']} -- {p['team']} ({p['position']})")
        
        choice = input(f"Select # (1-{len(results)}): ")
        try:
            return results[int(choice) - 1]
        except:
            return None
    except Exception as e:
        print(f"❌ Search Error: {e}")
        return None

def get_schedule_map(team_name):
    """
    Builds the Date/Opponent map for the specific team.
    """
    print(f"📅 Fetching Schedule for {team_name}...", end="\r")
    schedule_map = {}
    url = "https://api.collegefootballdata.com/games"

    for season_type in ['regular', 'postseason']:
        params = { "year": CURRENT_YEAR, "team": team_name, "seasonType": season_type }
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
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
                opponent = away if home == team_name else home
                if opponent is None: opponent = "TBD"
                    
                schedule_map[g_id] = { "date": fmt_date, "opponent": opponent, "week": game.get('week', 0) }
        except: pass
    return schedule_map

def get_stats_profile(position):
    """
    Decides which columns to show based on position.
    """
    if position == 'QB':
        return {
            'categories': ['passing', 'rushing'],
            'cols': ['Date', 'Wk', 'Opp', 'C/ATT', 'Pct', 'PasYds', 'PasTD', 'Int', 'Car', 'RusYds', 'RusTD']
        }
    else:
        # Default for RB, WR, TE, etc.
        return {
            'categories': ['rushing', 'receiving'],
            'cols': ['Date', 'Wk', 'Opp', 'Car', 'RusYds', 'RusTD', 'Rec', 'RecYds', 'RecTD']
        }

def get_player_game_stats(player_data):
    name = player_data['name']
    team = player_data['team']
    pos = player_data['position']
    
    # 1. Get Schedule & Profile
    game_map = get_schedule_map(team)
    profile = get_stats_profile(pos)
    print(f"\n🏈 --- FETCHING {pos} STATS: {name.upper()} ---")
    
    url = "https://api.collegefootballdata.com/games/players"
    all_rows = []

    # 2. Fetch Stats
    for season_type in ['regular', 'postseason']:
        # We request ALL categories so we don't miss anything (e.g. a WR throwing a pass)
        params = { "year": CURRENT_YEAR, "team": team, "seasonType": season_type }
        
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
            games_data = resp.json()

            for game in games_data:
                game_id = str(game.get('id'))
                
                # Match Schedule
                info = game_map.get(game_id, {'date': 'Unknown', 'opponent': 'Unknown', 'week': 0})
                
                # Data Container for this game
                # Initialize all possible stats to 0 or '-'
                stats = {
                    'Date': info['date'], 'Wk': info['week'], 'Opp': info['opponent'],
                    'C/ATT': '0/0', 'Pct': '0.0', 'PasYds': 0, 'PasTD': 0, 'Int': 0,
                    'Car': 0, 'RusYds': 0, 'RusTD': 0,
                    'Rec': 0, 'RecYds': 0, 'RecTD': 0
                }
                
                player_found = False
                
                # Parse the Box Score
                for t in game.get('teams', []):
                    # Check both 'school' and 'team' keys (API varies)
                    t_name = t.get('school') or t.get('team')
                    
                    if t_name == team:
                        for cat in t.get('categories', []):
                            cat_name = cat.get('name') # passing, rushing, receiving
                            
                            for stat_type in cat.get('types', []):
                                s_label = stat_type.get('name') # e.g., "C/ATT", "YDS"
                                
                                for ath in stat_type.get('athletes', []):
                                    if ath.get('name') == name:
                                        player_found = True
                                        val_str = ath.get('stat', '0')
                                        
                                        # --- LOGIC: MAP API LABELS TO OUR COLUMNS ---
                                        if cat_name == 'passing':
                                            if s_label == 'C/ATT': 
                                                stats['C/ATT'] = val_str
                                                # Calculate Percentage
                                                try:
                                                    c, a = map(int, val_str.split('/'))
                                                    stats['Pct'] = f"{(c/a)*100:.1f}" if a > 0 else "0.0"
                                                except: pass
                                            elif s_label == 'YDS': stats['PasYds'] = int(val_str)
                                            elif s_label == 'TD': stats['PasTD'] = int(val_str)
                                            elif s_label == 'INT': stats['Int'] = int(val_str)
                                            
                                        elif cat_name == 'rushing':
                                            if s_label == 'CAR': stats['Car'] = int(val_str)
                                            elif s_label == 'YDS': stats['RusYds'] = int(val_str)
                                            elif s_label == 'TD': stats['RusTD'] = int(val_str)
                                            
                                        elif cat_name == 'receiving':
                                            if s_label == 'REC': stats['Rec'] = int(val_str)
                                            elif s_label == 'YDS': stats['RecYds'] = int(val_str)
                                            elif s_label == 'TD': stats['RecTD'] = int(val_str)

                if player_found:
                    # Filter the dictionary to only the columns relevant to the position
                    row_data = {k: stats[k] for k in profile['cols']}
                    all_rows.append(row_data)

        except Exception as e:
            print(f"❌ Error parsing game: {e}")

    # 3. Output
    if all_rows:
        df = pd.DataFrame(all_rows)
        df = df.sort_values(by=['Date'])
        
        cols = profile['cols']
        # Dynamic Formatting String
        header_str = "  ".join([f"{c:<8}" if c not in ['Date', 'Opp'] else (f"{c:<12}" if c=='Date' else f"{c:<20}") for c in cols])
        
        print("\n" + "="*len(header_str))
        print(header_str)
        print("-" * len(header_str))
        
        for _, row in df.iterrows():
            row_str = "  ".join([f"{str(row[c]):<8}" if c not in ['Date', 'Opp'] else (f"{str(row[c]):<12}" if c=='Date' else f"{str(row[c]):<20}") for c in cols])
            print(row_str)
            
        print("="*len(header_str))
        
        fname = f"{name.replace(' ', '_')}_{pos}_{CURRENT_YEAR}.csv"
        df.to_csv(fname, index=False)
        print(f"\n💾 Saved to '{fname}'")
    else:
        print(f"❌ No stats found for {name}.")

if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        q = input("Enter Player Name (or 'q'): ").strip()
        if q.lower() == 'q': break
        
        p_data = search_player(q)
        if p_data:
            get_player_game_stats(p_data)