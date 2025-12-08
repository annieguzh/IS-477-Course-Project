# default target: run the full pipeline from acquisition to analysis & visualization
rule run_all:
    input:
        # Storage / organization summary
        "results/data_storage_summary.txt",
        # Integration summary
        "results/integrated_data_summary.txt",
        # Main analysis outputs
        "results/zip_level_summary.csv",
        "results/correlation_heatmap.png",
        "results/risk_correlations.txt",
        "results/high_risk_vs_zhvi_scatter.png",
        "results/low_risk_vs_zhvi_scatter.png",
        "results/housing_by_high_risk_tertiles.png",
        "results/housing_by_low_risk_tertiles.png",
        "results/risk_by_price_quartiles.csv"


# 1. Data acquisition

rule data_acquisition:
    output:
        "data/raw/food_inspections.csv",
        "data/raw/food_inspections.sha256",
        "data/raw/zhvi.csv",
        "data/raw/zhvi.sha256"
    shell:
        "python scripts/01_data_acquisition.py"



# 2. Storage & organization summary

rule data_storage:
    input:
        "data/raw/food_inspections.csv",
        "data/raw/zhvi.csv"
    output:
        "results/data_storage_summary.txt"
    shell:
        "python scripts/02_data_storage.py"



# 3. Data cleaning

rule clean_food:
    input:
        "data/raw/food_inspections.csv"
    output:
        "data/processed/food_inspections_cleaned.csv",
        "data/processed/food_inspections_cleaned.sha256"
    shell:
        "python scripts/03_data_cleaning_food.py"


rule clean_zhvi:
    input:
        "data/raw/zhvi.csv"
    output:
        "data/processed/zhvi_cleaned.csv",
        "data/processed/zhvi_cleaned.sha256"
    shell:
        "python scripts/03_data_cleaning_zhvi.py"



# 4. Data integration

rule integrate_data:
    input:
        "data/processed/food_inspections_cleaned.csv",
        "data/processed/zhvi_cleaned.csv"
    output:
        "data/processed/integrated_food_housing.csv",
        "data/processed/integrated_food_housing.sha256",
        "results/integrated_data_summary.txt"
    shell:
        "python scripts/04_data_integration.py"



# 5. Data analysis & visualization

rule analyze_visualize:
    input:
        "data/processed/integrated_food_housing.csv"
    output:
        "results/zip_level_summary.csv",
        "results/correlation_heatmap.png",
        "results/risk_correlations.txt",
        "results/high_risk_vs_zhvi_scatter.png",
        "results/low_risk_vs_zhvi_scatter.png",
        "results/housing_by_high_risk_tertiles.png",
        "results/housing_by_low_risk_tertiles.png",
        "results/risk_by_price_quartiles.csv"
    shell:
        "python scripts/05_data_analysis_visualization.py"
