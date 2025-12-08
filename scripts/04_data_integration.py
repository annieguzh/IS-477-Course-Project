# scripts/04_data_integration.py
import pandas as pd
import hashlib
from pathlib import Path

def main():
    PROCESSED_DIR = Path("data/processed")
    RESULTS_DIR = Path("results")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # collect printed lines for a summary file
    lines = []
    def log(msg=""):
        print(msg)
        lines.append(str(msg))

    # --- load cleaned inputs ---
    food_cleaned = pd.read_csv(PROCESSED_DIR / "food_inspections_cleaned.csv")
    zhvi_cleaned = pd.read_csv(PROCESSED_DIR / "zhvi_cleaned.csv")

    # --- prep ZHVI data ---
    zhvi_cleaned = zhvi_cleaned.rename(columns={"RegionName": "zip"})

    food_cleaned["zip"] = food_cleaned["zip"].astype(str)
    zhvi_cleaned["zip"] = zhvi_cleaned["zip"].astype(str)

    date_columns = [
        col for col in zhvi_cleaned.columns
        if isinstance(col, str) and "-" in col and len(col) == 10
    ]
    log(f"\nZHVI date columns: {len(date_columns)} (from {date_columns[0]} to {date_columns[-1]})")

    zhvi_cleaned["avg_zhvi_all_time"] = zhvi_cleaned[date_columns].mean(axis=1)

    recent_date_cols = [col for col in date_columns if col >= "2020-01-01"]
    zhvi_cleaned["avg_zhvi_recent"] = zhvi_cleaned[recent_date_cols].mean(axis=1)

    zhvi_cleaned["zhvi_latest"] = zhvi_cleaned[date_columns[-1]]
    latest_date = date_columns[-1]  # not used further, but nice to keep

    housing_columns = [
        "zip",
        "City",
        "State",
        "Metro",
        "CountyName",
        "avg_zhvi_all_time",
        "avg_zhvi_recent",
        "zhvi_latest",
    ]
    available_housing_cols = [col for col in housing_columns if col in zhvi_cleaned.columns]
    zhvi_for_merge = zhvi_cleaned[available_housing_cols].copy()

    log("\n=== PERFORMING INTEGRATION ===")

    # --- ZIP overlap check ---
    food_zips = set(food_cleaned["zip"].unique())
    housing_zips = set(zhvi_for_merge["zip"].unique())
    common_zips = food_zips & housing_zips

    log(f"\nZIP code overlap analysis:")
    log(f"  Food inspection ZIPs: {len(food_zips)}")
    log(f"  Housing ZIPs (all): {len(housing_zips)}")
    log(f"  ZIPs in BOTH datasets: {len(common_zips)}")
    log(f"  Food ZIPs not in housing: {len(food_zips - housing_zips)}")
    log(f"  Housing ZIPs not in food: {len(housing_zips - food_zips)}")

    # --- integrate ---
    integrated_data = pd.merge(
        food_cleaned,
        zhvi_for_merge,
        on="zip",
        how="inner",
        suffixes=("_food", "_housing"),
    )

    log(f"\nIntegration complete!")
    log(f"Integrated records: {len(integrated_data):,}")
    log(f"Integrated ZIP codes: {integrated_data['zip'].nunique()}")

    # --- post-integration analysis ---
    log("\n=== POST-INTEGRATION ANALYSIS ===")
    log(f"\nIntegrated Dataset:")
    log(f"  Total establishments: {len(integrated_data):,}")
    log(f"  Unique ZIP codes: {integrated_data['zip'].nunique()}")
    log(f"  Columns: {len(integrated_data.columns)}")

    establishments_per_zip = integrated_data.groupby("zip").size()
    log(f"\nEstablishments per ZIP code:")
    log(f"  Mean: {establishments_per_zip.mean():.1f}")
    log(f"  Median: {establishments_per_zip.median():.0f}")
    log(f"  Min: {establishments_per_zip.min()}")
    log(f"  Max: {establishments_per_zip.max()}")

    log(f"\nRisk distribution in integrated data:")
    log(integrated_data["risk"].value_counts())

    log(f"\nHousing value statistics (latest ZHVI):")
    log(f"  Mean: ${integrated_data['zhvi_latest'].mean():,.0f}")
    log(f"  Median: ${integrated_data['zhvi_latest'].median():,.0f}")
    log(f"  Min: ${integrated_data['zhvi_latest'].min():,.0f}")
    log(f"  Max: ${integrated_data['zhvi_latest'].max():,.0f}")

    log(f"\nTop 5 facility types in integrated data:")
    log(integrated_data["facility_type"].value_counts().head())

    # --- write integrated dataset ---
    output_file = PROCESSED_DIR / "integrated_food_housing.csv"
    integrated_data.to_csv(output_file, index=False)

    with open(output_file, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(PROCESSED_DIR / "integrated_food_housing.sha256", "w", encoding="utf-8") as f:
        f.write(sha)

    # --- write summary text file ---
    summary_path = RESULTS_DIR / "integrated_data_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(str(line) + "\n")

    log(f"\n[INFO] Integration summary written to {summary_path}")

if __name__ == "__main__":
    main()
