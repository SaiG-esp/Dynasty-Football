import pandas as pd
import requests
import io
import os

def verify_2024_stats():
    # 1. The EXACT 2024 link you provided
    url = "https://raw.githubusercontent.com/sportsdataverse/cfbfastR-data/refs/heads/main/player_stats/csv/player_stats_2024.csv"
    local_file = "stats_2024_raw.csv"

    print(f"⬇️ Downloading 2024 Stats for Verification...")
    
    try:
        # Check if we already have it locally
        if os.path.exists(local_file):
            print("✅ Found local file. Loading...")
            df = pd.read_csv(local_file)
        else:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Connection established! Parsing data...")
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(local_file, index=False)
            else:
                print(f"❌ Error: Server returned {response.status_code}")
                return

        # 2. FILTER: Focus on Receivers (Player who caught the ball)
        # We drop rows where 'reception_player' is missing (e.g. run plays, incomplete passes)
        rec_df = df.dropna(subset=['reception_player']).copy()
        
        # 3. AGGREGATE: Group by Player to get Season Totals
        season_stats = rec_df.groupby(['reception_player', 'team']).agg(
            Receptions=('reception_player', 'count'),      # Count rows = Receptions
            Yards=('reception_yds', 'sum'),                # Sum yards
            Touchdowns=('touchdown_stat', 'sum')           # Sum TDs
        ).reset_index()

        # Sort by Yards to see the stars
        season_stats = season_stats.sort_values(by='Yards', ascending=False)
        
        # 4. Show Ohio State's Top Receivers for Cross-Check
        print("\n--- 🏈 Ohio State 2024 Verification ---")
        osu_wr = season_stats[season_stats['team'] == 'Ohio State']
        print(osu_wr.head(5).to_string(index=False))

        # 5. AUTOMATIC AUDIT: Check Jeremiah Smith's stats specifically
        # (Official 2024 Stats: ~76 Rec, ~1315 Yds, ~15 TDs)
        js = osu_wr[osu_wr['reception_player'] == 'Jeremiah Smith']
        
        if not js.empty:
            print("\n--- 🕵️‍♂️ AUDIT: Jeremiah Smith ---")
            print(f"Your Script Found: {int(js['Receptions'].values[0])} Rec, {int(js['Yards'].values[0])} Yds, {int(js['Touchdowns'].values[0])} TDs")
            print("Official Reference: 76 Rec, 1315 Yds, 15 TDs")
            
            # Simple check
            if int(js['Yards'].values[0]) == 1315:
                print("✅ PERFECT MATCH. Your engine is accurate.")
            else:
                print("⚠️ Mismatch. Check if bowl games or conference championships are included/excluded.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_2024_stats()