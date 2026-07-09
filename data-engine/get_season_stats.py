import requests
import pandas as pd
import warnings

# 1. SSL/WARNING FIX
# This suppresses the red warning text so your terminal stays clean
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

# --- CONFIGURATION ---
from config import API_KEY

PLAYER_TARGET = "Jeremiah Smith"
TEAM_TARGET = "Ohio State"
YEAR = 2024

def get_player_box_score():
    print(f"\n🏈 --- 2024 OFFICIAL BOX SCORES: {PLAYER_TARGET.upper()} ---")
    
    headers = { "Authorization": f"Bearer {API_KEY}" }
    url = "https://api.collegefootballdata.com/games/players"
    
    all_game_rows = []

    # 2. LOOP THROUGH SEASONS
    for season_type in ['regular', 'postseason']:
        print(f"📡 Fetching {season_type.title()} Season...", end="\r")
        
        params = {
            "year": YEAR,
            "team": TEAM_TARGET,
            "seasonType": season_type,
            "category": "receiving"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"⚠️ API Error ({response.status_code})")
                continue

            games_data = response.json()

            # 3. PARSE EACH GAME
            for game in games_data:
                # SAFE GUARD: Default to 0 if week is missing/null to prevent formatting crash
                week = game.get('week') 
                if week is None:
                    week = 0
                
                opponent = "Unknown"
                rec, yds, td = 0, 0, 0
                player_found_in_game = False
                
                teams_list = game.get('teams', [])
                
                # First pass: Find the Opponent
                for t in teams_list:
                    # FIX: Use 'team' instead of 'school'
                    team_name = t.get('team')
                    # Ensure team_name is a string before checking to prevent crashes
                    if team_name and isinstance(team_name, str) and team_name != TEAM_TARGET:
                        opponent = team_name
                
                # Second pass: Find Player Stats
                for t in teams_list:
                    if t.get('team') == TEAM_TARGET:
                        for category in t.get('categories', []):
                            if category.get('name') == 'receiving':
                                
                                # Loop through stats (REC, YDS, TD)
                                for stat_type in category.get('types', []):
                                    stat_name = stat_type.get('name')
                                    
                                    # Check athletes
                                    for athlete in stat_type.get('athletes', []):
                                        if athlete.get('name') == PLAYER_TARGET:
                                            player_found_in_game = True
                                            try:
                                                # Safely convert string stat to int
                                                val = int(athlete.get('stat', 0))
                                                if stat_name == 'REC': rec = val
                                                elif stat_name == 'YDS': yds = val
                                                elif stat_name == 'TD': td = val
                                            except:
                                                pass

                if player_found_in_game:
                    all_game_rows.append({
                        "Type": "P" if season_type == 'postseason' else "R",
                        "Week": week,
                        "Opponent": opponent,
                        "Rec": rec,
                        "Yds": yds,
                        "TD": td
                    })

        except Exception as e:
            print(f"\n❌ Error: {e}")

    # 4. OUTPUT RESULTS
    if all_game_rows:
        df = pd.DataFrame(all_game_rows)
        # Sort by Type (Regular first), then Week
        df = df.sort_values(by=['Type', 'Week'], ascending=[False, True]) 

        print("\n" + "="*55)
        print(f"{'WK':<4} {'OPPONENT':<20} {'REC':<5} {'YDS':<5} {'TD':<5}")
        print("-" * 55)
        
        for index, row in df.iterrows():
            print(f"{row['Week']:<4} {row['Opponent']:<20} {row['Rec']:<5} {row['Yds']:<5} {row['TD']:<5}")

        print("-" * 55)
        print(f"{'TOTAL':<25} {df['Rec'].sum():<5} {df['Yds'].sum():<5} {df['TD'].sum():<5}")
        print("="*55)
        
        # Save to CSV for your website
        filename = "jeremiah_smith_2024.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ Success! Data saved to '{filename}'")
        
    else:
        print("\n❌ Still no stats found. Verify strict spelling of 'Jeremiah Smith'.")

if __name__ == "__main__":
    get_player_box_score()