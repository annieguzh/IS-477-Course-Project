# scripts/03_data_cleaning_zhvi.py

import pandas as pd
import hashlib
from pathlib import Path

def main():
    RAW_DIR = Path("data/raw")
    PROCESSED_DIR = Path("data/processed")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    zhvi = pd.read_csv(RAW_DIR / "zhvi.csv")


    zhvi_cleaned = zhvi.copy()

    print("\n=== IDENTIFYING DATE COLUMNS ===")
    all_columns = zhvi_cleaned.columns.tolist()
    date_columns = [col for col in all_columns if isinstance(col, str) and '-' in col and len(col) == 10]
    metadata_columns = [col for col in all_columns if col not in date_columns]
    print(f"Total date columns: {len(date_columns)}")
    print(f"Date range: {date_columns[0]} to {date_columns[-1]}")
    print(f"Metadata columns: {metadata_columns}")

    print("\n=== HANDLING MISSING VALUES ===")

    # Check missing values in date columns
    missing_per_row = zhvi_cleaned[date_columns].isnull().sum(axis=1)
    print(f"Missing value statistics per ZIP code:")
    print(f"  Mean missing: {missing_per_row.mean():.1f} months")
    print(f"  Median missing: {missing_per_row.median():.0f} months")
    print(f"  Max missing: {missing_per_row.max():.0f} months")

    # remove ZIP codes with >80% missing values
    threshold = len(date_columns) * 0.8
    initial_count = len(zhvi_cleaned)
    zhvi_cleaned = zhvi_cleaned[missing_per_row <= threshold]
    removed = initial_count - len(zhvi_cleaned)
    print(f"\nRemoved {removed} ZIP codes with >80% missing values")
    print(f"Remaining ZIP codes: {len(zhvi_cleaned):,}")


    print("\n=== REMOVING ZIP CODES WITH NO RECENT DATA ===")
    recent_months = date_columns[-12:]
    print(f"Checking recent months: {recent_months[0]} to {recent_months[-1]}")

    # Count missing values in recent 12 months
    recent_missing = zhvi_cleaned[recent_months].isnull().sum(axis=1)

    # Remove ZIP codes with no data in all 12 recent months
    initial_count = len(zhvi_cleaned)
    zhvi_cleaned = zhvi_cleaned[recent_missing < 12]
    removed = initial_count - len(zhvi_cleaned)
    print(f"Removed {removed} ZIP codes with NO data in recent 12 months")
    print(f"Remaining ZIP codes: {len(zhvi_cleaned):,}")

    print("\n=== FINAL DATA SUMMARY ===")

    print(f"\nTotal ZIP codes: {len(zhvi_cleaned):,}")
    print(f"Total columns: {len(zhvi_cleaned.columns)}")
    print(f"Date coverage: {date_columns[0]} to {date_columns[-1]}")

    

    output_file = PROCESSED_DIR / "zhvi_cleaned.csv"
    zhvi_cleaned.to_csv(output_file, index=False)

    with open(output_file, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(PROCESSED_DIR / "zhvi_cleaned.sha256", "w", encoding="utf-8") as f:
        f.write(sha)

if __name__ == "__main__":
    main()
