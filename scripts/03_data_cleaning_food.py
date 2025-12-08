# scripts/03_data_cleaning_food.py

import pandas as pd
import hashlib
from pathlib import Path

def main():
    RAW_DIR = Path("data/raw")
    PROCESSED_DIR = Path("data/processed")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    chicago_food_inspection = pd.read_csv(RAW_DIR / "food_inspections.csv")

    food_cleaned = chicago_food_inspection.copy()
    food_cleaned = food_cleaned.dropna()

    # --- convert inspection_date to datetime ---
    food_cleaned["inspection_date"] = pd.to_datetime(
        food_cleaned["inspection_date"], errors="coerce"
    )
    invalid_dates = food_cleaned["inspection_date"].isnull().sum()
    if invalid_dates > 0:
        print(f"Removing {invalid_dates} records with invalid dates...")
        food_cleaned = food_cleaned.dropna(subset=["inspection_date"])
    print(
        f"Date range: {food_cleaned['inspection_date'].min()} "
        f"to {food_cleaned['inspection_date'].max()}"
    )

    # --- keep only the latest inspection for each establishment ---
    print("\nIdentifying establishments by:")
    print(f"  - DBA name: {food_cleaned['dba_name'].nunique():,} unique")
    print(f"  - License number: {food_cleaned['license_'].nunique():,} unique")
    print(f"  - Address: {food_cleaned['address'].nunique():,} unique")

    # Create a unique establishment ID based on license + address (as strings)
    food_cleaned["establishment_id"] = (
        food_cleaned["license_"].fillna("UNKNOWN").astype(str)
        + "_"
        + food_cleaned["address"].fillna("UNKNOWN").astype(str)
    )

    print(f"\nTotal inspection records before: {len(food_cleaned):,}")
    print(f"Unique establishments: {food_cleaned['establishment_id'].nunique():,}")

    # Sort by inspection date (most recent first) and keep first record per establishment
    food_cleaned = (
        food_cleaned
        .sort_values("inspection_date", ascending=False)
        .groupby("establishment_id", as_index=False)
        .first()
    )
    # Drop helper column
    food_cleaned = food_cleaned.drop(columns=["establishment_id"])
    print("\nKept only the latest inspection per establishment")

    # --- clean ZIP codes ---
    food_cleaned["zip"] = food_cleaned["zip"].astype(str).str[:5]
    food_cleaned["zip"] = food_cleaned["zip"].str.replace(r"\D", "", regex=True)

    initial_count = len(food_cleaned)
    food_cleaned = food_cleaned[
        (food_cleaned["zip"].str.len() == 5)
        & (~food_cleaned["zip"].str.startswith("000"))
    ]
    removed = initial_count - len(food_cleaned)
    print(f"Removed {removed} records with invalid ZIP codes")
    print(f"Remaining records: {len(food_cleaned):,}")
    print(f"Unique ZIP codes: {food_cleaned['zip'].nunique()}")

    print("\nSample ZIP codes:")
    print(food_cleaned["zip"].value_counts().head(10))

    columns_to_keep = [
        "inspection_id",
        "dba_name",
        "aka_name",
        "license_",
        "facility_type",
        "risk",
        "address",
        "city",
        "state",
        "zip",
        "inspection_date",
        "inspection_type",
        "results",
        "violations",
        "latitude",
        "longitude",
    ]
    available_columns = [col for col in columns_to_keep if col in food_cleaned.columns]
    food_cleaned = food_cleaned[available_columns].copy()

    print("=== CLEANED DATA SUMMARY ===\n")
    print(f"Total records: {len(food_cleaned):,}")
    print(f"Unique establishments (one per row): {len(food_cleaned):,}")
    print(f"Unique ZIP codes: {food_cleaned['zip'].nunique()}")
    print(
        f"Date range: {food_cleaned['inspection_date'].min()} "
        f"to {food_cleaned['inspection_date'].max()}"
    )

    print("\nRisk distribution:")
    print(food_cleaned["risk"].value_counts())

    print("\nInspection results distribution:")
    print(food_cleaned["results"].value_counts().head(10))

    print("\nTop facility types:")
    print(food_cleaned["facility_type"].value_counts().head(10))

    print("\nMissing values:")
    missing = food_cleaned.isnull().sum()
    print(missing[missing > 0])

    # --- write outputs ---
    output_file = PROCESSED_DIR / "food_inspections_cleaned.csv"
    food_cleaned.to_csv(output_file, index=False)

    with open(output_file, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(
        PROCESSED_DIR / "food_inspections_cleaned.sha256",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(sha)

if __name__ == "__main__":
    main()
