# scripts/01_data_acquisition.py
import requests
import pandas as pd
import hashlib
from pathlib import Path

def main():
    OUTPUT_DIR = Path("data/raw")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -- Chicago Food Inspections --
    API_ENDPOINT = "https://data.cityofchicago.org/resource/4ijn-s7e5.json"
    all_records = []
    limit = 50000  
    offset = 0

    while True:
        params = {
            "$limit": limit,
            "$offset": offset,
            "$order": "inspection_date DESC"
        }
        print(f"Fetching records {offset} to {offset + limit}...")
        resp = requests.get(API_ENDPOINT, params=params)
        resp.raise_for_status()
        payload = resp.json()
    
        if len(payload) == 0:
            break
        
        all_records.extend(payload)
        print(f"  Retrieved {len(payload)} records (Total so far: {len(all_records)})")

        if len(payload) < limit:
            break
        
        offset += limit
    print(f"\nSuccessfully fetched {len(all_records)} total records")

    chicago_food_inspection = pd.json_normalize(all_records)

    food_path = OUTPUT_DIR / "food_inspections.csv"
    chicago_food_inspection.to_csv(food_path, index=False)

    with open(food_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(OUTPUT_DIR / "food_inspections.sha256", "w", encoding="utf-8") as f:
        f.write(sha)


    # -- ZHVI CSV --
    csv_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1762826225"   # the Zillow URL you used
    response = requests.get(csv_url)
    zhvi_path = OUTPUT_DIR / "zhvi.csv"
    with open(zhvi_path, "wb") as f:
        f.write(response.content)

    with open(zhvi_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(OUTPUT_DIR / "zhvi.sha256", "w", encoding="utf-8") as f:
        f.write(sha)

if __name__ == "__main__":
    main()