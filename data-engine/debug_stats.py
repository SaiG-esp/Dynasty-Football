import pandas as pd
import os

def debug_mismatch():
    csv_file = "stats_2024_raw.csv" # The file we downloaded earlier
    
    if not os.path.exists(csv_file):
        print("❌ File not found. Run the download script first.")
        return

    print("🕵️ LOADING DATA FOR DIAGNOSTICS...")
    # Load everything. No filters. No dropna.
    df = pd.read_csv(csv_file, low_memory=False)
    
    # 1. FUZZY SEARCH: Find ANY row involving Jeremiah Smith
    # We look at the 'reception_player' column specifically
    print("\n--- 1. NAME CHECK ---")
    # Get all unique names that look like "Smith"
    all_names = df['reception_player'].dropna().unique()
    smiths = [n for n in all_names if 'Jeremiah' in str(n) and 'Smith' in str(n)]
    print(f"Variations of 'Jeremiah Smith' found in column: {smiths}")
    
    # 2. WEEKLY BREAKDOWN (The Smoking Gun)
    # We filter for his main name and see what weeks we have
    print("\n--- 2. WEEKLY LOG (Jeremiah Smith) ---")
    
    # Filter for him (using the first name found)
    js_df = df[df['reception_player'] == 'Jeremiah Smith'].copy()
    
    # Group by WEEK to see where the data stops
    weekly = js_df.groupby(['week', 'opponent']).agg(
        Plays=('play_id', 'count'),
        Yards=('reception_yds', 'sum'),
        TDs=('touchdown_stat', 'sum')
    ).reset_index().sort_values('week')
    
    print(weekly.to_string(index=False))
    
    print(f"\nTotal Yards Found: {weekly['Yards'].sum()}")
    
    # 3. CHECK FOR "GHOST" ROWS
    # Sometimes he is the TARGET but not the RECEPTION_PLAYER (e.g. penalties, drops?)
    # or maybe the reception_player name is blank but the ID is there?
    print("\n--- 3. GHOST ROW CHECK ---")
    # Let's check if there are rows where he is the 'target_player' but reception_yds > 0
    # and he is NOT listed as the reception_player
    ghosts = df[
        (df['target_player'] == 'Jeremiah Smith') & 
        (df['reception_yds'] > 0) & 
        (df['reception_player'] != 'Jeremiah Smith')
    ]
    
    if not ghosts.empty:
        print(f"⚠️ FOUND {len(ghosts)} GHOST PLAYS!")
        print("These are plays where he was targeted, yards were gained, but he wasn't listed as the receiver.")
        print(ghosts[['week', 'desc', 'reception_player', 'reception_yds']].head())
    else:
        print("✅ No ghost rows found (Targeted + Yards, but wrong name).")

if __name__ == "__main__":
    debug_mismatch()