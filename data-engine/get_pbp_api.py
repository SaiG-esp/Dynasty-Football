import requests
import pandas as pd

def get_pbp_direct():
    # 1. YOUR KEY
    api_key = "RB6XKAKaHDQniZB8mLcR4jP30+NeVZw/YCEZcBKeSpKIYuZmBNhswNNkBHLvNxf1"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    print("🏈 Contacting API via direct HTTP request...")

    # 2. Request Data (Ohio State, 2024, Week 1)
    url = "https://api.collegefootballdata.com/plays"
    params = { "year": 2024, "week": 1, "team": "Ohio State" }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print("✅ Success! 200 OK - Data Downloaded.")
            data = response.json()
            df = pd.DataFrame(data)
            
            # 3. FIX: Use the EXACT column names from your screenshot
            # We use 'playText' for the description
            # We use 'yardsGained' (camelCase) for the yards
            
            print(f"📊 Analyzing {len(df)} plays...")

            # 4. Filter for Jeremiah Smith
            js = df[
                df['playText'].str.contains("Jeremiah Smith", case=False, na=False)
            ]
            
            print(f"🌰 Found {len(js)} Jeremiah Smith plays.")
            
            # Show the result using the CORRECT columns
            if not js.empty:
                print("\n--- Play Preview ---")
                # selecting: period, playText, and yardsGained
                print(js[['period', 'playText', 'yardsGained']].head())
                
                total_yards = js['yardsGained'].sum()
                print(f"\n📈 Total Yards Found: {total_yards}")
            else:
                print("No plays found (check spelling or week).")
            
            # Save
            df.to_csv("osu_pbp_direct.csv", index=False)
            print("\n💾 Saved to 'osu_pbp_direct.csv'")
            
        else:
            print(f"❌ Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Python Error: {e}")

if __name__ == "__main__":
    get_pbp_direct()