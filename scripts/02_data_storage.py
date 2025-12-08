# scripts/02_data_storage.py

from pathlib import Path
import pandas as pd

def main():
    RAW_DIR = Path("data/raw")
    PROCESSED_DIR = Path("data/processed")
    RESULTS_DIR = Path("results")

    
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    food_path = RAW_DIR / "food_inspections.csv"
    zhvi_path = RAW_DIR / "zhvi.csv"

    chicago_food_inspection = pd.read_csv(food_path)
    zhvi = pd.read_csv(zhvi_path)

    # --- Build storage & organization report text ---
    lines = []

    lines.append("DATA STORAGE AND ORGANIZATION OVERVIEW")
    lines.append("=====================================")
    lines.append("")
    lines.append("Filesystem layout:")
    lines.append("  data/raw/        - Raw source files as downloaded (API dumps, original CSVs)")
    lines.append("  data/processed/  - Cleaned and integrated datasets used for analysis")
    lines.append("  results/         - Derived artifacts (summaries, plots, analysis outputs)")
    lines.append("")
    lines.append("Naming conventions:")
    lines.append("  * Raw files:        data/raw/<dataset_name>.csv")
    lines.append("  * Processed files:  data/processed/<dataset_name>_cleaned.csv or integrated_*.csv")
    lines.append("  * Checksums:        matching .sha256 files next to raw/processed data")
    lines.append("  * Results:          results/*.csv, results/*.txt, results/*.png")
    lines.append("")
    lines.append("=== FOOD INSPECTIONS (data/raw/food_inspections.csv) ===")
    lines.append(f"Total records: {len(chicago_food_inspection)}")
    lines.append(f"Number of columns: {len(chicago_food_inspection.columns)}")
    lines.append(f"Columns: {chicago_food_inspection.columns.tolist()}")

    if "zip" in chicago_food_inspection.columns:
        lines.append(f"Unique ZIP codes: {chicago_food_inspection['zip'].nunique()}")
    else:
        lines.append("Unique ZIP codes: N/A (no 'zip' column found)")

    lines.append("")
    lines.append("=== ZILLOW ZHVI (data/raw/zhvi.csv) ===")
    lines.append(f"Total records: {len(zhvi)}")

    if "City" in zhvi.columns:
        lines.append("Top 5 cities by record count:")
        lines.append(str(zhvi["City"].value_counts().head()))
        lines.append(f"Chicago records: {len(zhvi[zhvi['City'] == 'Chicago'])}")
    else:
        lines.append("City breakdown: N/A (no 'City' column found)")

    lines.append("")

    # --- Write report to results/ ---
    report_path = RESULTS_DIR / "data_storage_summary.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(str(line) + "\n")

    print("\n".join(lines))
    print(f"\n[INFO] Storage summary written to {report_path}")

if __name__ == "__main__":
    main()
