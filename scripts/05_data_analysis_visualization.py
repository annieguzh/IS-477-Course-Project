# scripts/05_data_analysis_visualization.py

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    PROCESSED_DIR = Path("data/processed")
    RESULTS_DIR = Path("results")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    integrated_data = pd.read_csv(PROCESSED_DIR / "integrated_food_housing.csv")

    risk_counts = (
        integrated_data
        .groupby(["zip", "risk"])
        .size()
        .reset_index(name="n_inspections")
    )

    risk_pivot = (
        risk_counts
        .pivot(index="zip", columns="risk", values="n_inspections")
        .fillna(0)
    )

    risk_pivot = risk_pivot.rename(columns={
        "Risk 1 (High)": "high_risk_count",
        "Risk 2 (Medium)": "medium_risk_count",
        "Risk 3 (Low)": "low_risk_count",
    })

    risk_pivot["total_inspections"] = (
        risk_pivot["high_risk_count"] +
        risk_pivot["medium_risk_count"] +
        risk_pivot["low_risk_count"]
    )

    risk_pivot["high_risk_prop"]   = risk_pivot["high_risk_count"]   / risk_pivot["total_inspections"]
    risk_pivot["medium_risk_prop"] = risk_pivot["medium_risk_count"] / risk_pivot["total_inspections"]
    risk_pivot["low_risk_prop"]    = risk_pivot["low_risk_count"]    / risk_pivot["total_inspections"]

    # attach housing data at ZIP level
    housing_zip = (
        integrated_data
        .groupby("zip")[["avg_zhvi_all_time", "avg_zhvi_recent", "zhvi_latest"]]
        .mean()
        .reset_index()
    )

    zip_level = (
        risk_pivot
        .reset_index()
        .merge(housing_zip, on="zip", how="inner")
    )

    # 1) save table
    zip_level.to_csv(RESULTS_DIR / "zip_level_summary.csv", index=False)

    # 2) correlation + save to text
    corr_cols = [
        "high_risk_prop",
        "medium_risk_prop",
        "low_risk_prop",
        "avg_zhvi_all_time",
        "avg_zhvi_recent",
        "zhvi_latest",
        "total_inspections",
    ]

    # Compute correlation matrix
    corr = zip_level[corr_cols].corr()

    # Round to 2 decimals for annotation
    annot_matrix = corr.round(2)

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(
        corr,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        annot=annot_matrix, 
        fmt="",              
        annot_kws={"size": 8, "color": "black"}
    )
    ax.set_title("Correlation: risk proportions and housing values (ZIP level)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()


    # Correlations between risk proportions and recent ZHVI
    r_high = zip_level["high_risk_prop"].corr(zip_level["avg_zhvi_recent"])
    r_low  = zip_level["low_risk_prop"].corr(zip_level["avg_zhvi_recent"])
    r_med  = zip_level["medium_risk_prop"].corr(zip_level["avg_zhvi_recent"])

    with open(RESULTS_DIR / "risk_correlations.txt", "w") as f:
        f.write("Pearson correlations (computed via pandas.DataFrame.corr)\n")
        f.write(f"High-risk prop vs avg_zhvi_recent: r = {r_high:.3f}\n")
        f.write(f"Low-risk  prop vs avg_zhvi_recent: r = {r_low:.3f}\n")
        f.write(f"Medium-risk prop vs avg_zhvi_recent: r = {r_med:.3f}\n")


    # 3) save scatter plot
    plt.figure()
    sns.regplot(
        data=zip_level,
        x="high_risk_prop",
        y="avg_zhvi_recent",
        scatter_kws={"alpha": 0.7},
        line_kws={"color": "red"}
    )
    plt.xlabel("Proportion of high-risk inspections (per ZIP)")
    plt.ylabel("Average ZHVI (recent years, USD)")
    plt.title("High-risk share vs housing values")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "high_risk_vs_zhvi_scatter.png", dpi=300)
    plt.close()

    plt.figure()
    sns.regplot(
        data=zip_level,
        x="low_risk_prop",
        y="avg_zhvi_recent",
        scatter_kws={"alpha": 0.7},
        line_kws={"color": "green"}
    )
    plt.xlabel("Proportion of low-risk inspections (per ZIP)")
    plt.ylabel("Average ZHVI (recent years, USD)")
    plt.title("Low-risk share vs housing values")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "low_risk_vs_zhvi_scatter.png", dpi=300)
    plt.close()


    # Create tertiles (low / medium / high) based on risk proportions
    zip_level["high_risk_tertile"] = pd.qcut(
        zip_level["high_risk_prop"],
        q=3,
        labels=["Low high-risk", "Medium high-risk", "High high-risk"]
    )

    zip_level["low_risk_tertile"] = pd.qcut(
        zip_level["low_risk_prop"],
        q=3,
        labels=["Low low-risk", "Medium low-risk", "High low-risk"]
    )

    # Boxplot: housing by high-risk tertiles
    plt.figure(figsize=(7, 5))
    order_high = ["Low high-risk", "Medium high-risk", "High high-risk"]
    sns.boxplot(
        data=zip_level,
        x="high_risk_tertile",
        y="avg_zhvi_recent",
        order=order_high
    )
    sns.stripplot(
        data=zip_level,
        x="high_risk_tertile",
        y="avg_zhvi_recent",
        order=order_high,
        color="black",
        size=3,
        alpha=0.5
    )
    plt.xlabel("ZIP groups by high-risk proportion")
    plt.ylabel("Average ZHVI (recent years, USD)")
    plt.title("Housing values across ZIPs with different high-risk shares")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "housing_by_high_risk_tertiles.png", dpi=300)
    plt.close()

    # Boxplot: housing by low-risk tertiles
    plt.figure(figsize=(7, 5))
    order_low = ["Low low-risk", "Medium low-risk", "High low-risk"]
    sns.boxplot(
        data=zip_level,
        x="low_risk_tertile",
        y="avg_zhvi_recent",
        order=order_low
    )
    sns.stripplot(
        data=zip_level,
        x="low_risk_tertile",
        y="avg_zhvi_recent",
        order=order_low,
        color="black",
        size=3,
        alpha=0.5
    )
    plt.xlabel("ZIP groups by low-risk proportion")
    plt.ylabel("Average ZHVI (recent years, USD)")
    plt.title("Housing values across ZIPs with different low-risk shares")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "housing_by_low_risk_tertiles.png", dpi=300)
    plt.close()


    # risk proportions by housing price quartile
    zip_level["zhvi_quartile"] = pd.qcut(
        zip_level["avg_zhvi_recent"],
        q=4,
        labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
    )

    risk_by_price = (
        zip_level
        .groupby("zhvi_quartile")[["high_risk_prop", "low_risk_prop", "medium_risk_prop"]]
        .mean()
        .reindex(["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
    )

    print("Average risk proportions by housing price quartile:")
    print(risk_by_price)
    risk_by_price.to_csv(RESULTS_DIR / "risk_by_price_quartiles.csv")



if __name__ == "__main__":
    main()
