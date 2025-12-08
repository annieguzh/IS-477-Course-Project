# Data Analysis and Visualization Documentation

### 1\. Scripts used

All analysis and visualization logic is implemented in:

* **scripts/05\_data\_analysis\_visualization.py**

This script:

* Reads the integrated establishment‑level dataset from data/processed/integrated\_food\_housing.csv.

* Aggregates data to the ZIP‑code level and calculates the proportions of high‑, medium‑, and low‑risk inspections per ZIP.

* Merges these risk proportions with ZIP‑level housing value metrics (ZHVI).

* Produces a summary table, correlation statistics, and multiple publication‑quality figures.

* Writes all outputs to the results/ directory.

### 2\. Analysis steps

1. Aggregate inspections to ZIP level  
   1. The script groups the integrated data by zip and risk to count how many inspections fall into each risk category in each ZIP code.  
   2. These counts are pivoted into a wide format so each ZIP has separate columns for the counts of “Risk 1 (High)”, “Risk 2 (Medium)”, and “Risk 3 (Low)”.  
   3. A total\_inspections column is computed as the sum of these three counts.  
   4. Proportions for each risk category are derived by dividing each count by total\_inspections, creating high\_risk\_prop, medium\_risk\_prop, and low\_risk\_prop for each ZIP.

2. Attach housing value metrics  
   1. Using the integrated dataset, the script computes ZIP‑level averages for the housing variables:  
      1. Avg\_zhvi\_all\_time  
      2. Avg\_zhvi\_recent  
      3. zhvi\_latest  
   2. These are merged with the risk‑proportion table on zip to produce a single ZIP‑level analysis table (zip\_level).  
   3. This table is saved as results/zip\_level\_summary.csv for use in the report or further exploration.

3. Correlation analysis  
   1. The script computes a correlation matrix between:  
      1. Risk proportions (high\_risk\_prop, medium\_risk\_prop, low\_risk\_prop)  
      2. Housing metrics (avg\_zhvi\_all\_time, avg\_zhvi\_recent, zhvi\_latest)  
      3. total\_inspections  
   2. A rounded version of this matrix is used as annotations in a heatmap, and the complete correlation matrix is used to interpret the strength and direction of relationships.

   3. In addition, simple Pearson correlations between each risk proportion and avg\_zhvi\_recent are computed and written to results/risk\_correlations.txt. This file records the numerical values (e.g., r=0.62 for high risk, r=-0.55 for low risk) that we report in the narrative analysis.

4. Scatterplots with fitted trend lines  
   1. To visualize the relationship between risk proportions and housing values, the script generates two scatterplots with regression lines:  
      1. High‑risk share vs housing values: high\_risk\_prop on the x‑axis and avg\_zhvi\_recent on the y‑axis.  
      2. Low‑risk share vs housing values: low\_risk\_prop on the x‑axis and avg\_zhvi\_recent on the y‑axis.  
   2. These plots show whether ZIPs with more high‑risk (or low‑risk) inspections tend to have higher or lower home values.  
   3. Each figure is saved as a PNG in the results/ directory:  
      1. High\_risk\_vs\_zhvi\_scatter.png  
      2. low\_risk\_vs\_zhvi\_scatter.png

5. Risk‑based ZIP groups and boxplots  
   1. The script divides ZIP codes into three groups (tertiles) based on:  
      1. high\_risk\_prop \-\> Low high-risk, Medium high-risk, High high-risk  
      2. low\_risk\_prop \-\> Low low-risk, Medium low-risk, High low-risk

   2. For each set of tertiles, it plots boxplots of avg\_zhvi\_recent by group, with overlaid strip points to show individual ZIP values:  
      1. Housing values across high‑risk tertiles \-\> housing\_by\_high\_risk\_tertiles.png  
      2. Housing values across low‑risk tertiles \-\> housing\_by\_low\_risk\_tertiles.png

   3. These visualizations highlight how the distribution of housing values shifts when moving from ZIPs with low to high shares of high‑risk or low‑risk inspections.

6. Risk proportions by housing price quartile  
   1. The script further groups ZIP codes into four quartiles based on avg\_zhvi\_recent (from lowest to highest housing prices).  
   2. For each housing price quartile, it computes the mean high\_risk\_prop, medium\_risk\_prop, and low\_risk\_prop.  
   3. The resulting table is printed to the console and saved as results/risk\_by\_price\_quartiles.csv.  
   4. This table provides a concise numerical summary, e.g., showing that the highest‑price quartile tends to have a higher mean high‑risk proportion and a lower mean low‑risk proportion than the lowest‑price quartile.

### 3\. Analysis results and visualizations produced

Running scripts/05\_data\_analysis\_visualization.py (or the Snakemake rule that calls it) produces the following key artifacts in results/:

* Tables and numeric summaries  
  * zip\_level\_summary.csv – ZIP‑level table with risk proportions and housing metrics.  
  * risk\_correlations.txt – Pearson correlation coefficients between risk proportions and housing values.  
  * risk\_by\_price\_quartiles.csv – average risk proportions within each housing price quartile.

* Figures  
  * correlation\_heatmap.png – heatmap of correlations between risk proportions, housing metrics, and inspection counts.  
  * high\_risk\_vs\_zhvi\_scatter.png – scatterplot with regression line for high‑risk share vs housing values.  
  * low\_risk\_vs\_zhvi\_scatter.png – scatterplot with regression line for low‑risk share vs housing values.  
  * housing\_by\_high\_risk\_tertiles.png – boxplot of housing values by high‑risk tertiles.  
  * housing\_by\_low\_risk\_tertiles.png – boxplot of housing values by low‑risk tertiles.

Together, these outputs support the project’s main conclusion: at the ZIP level, higher proportions of high‑risk inspections are associated with higher housing values, while higher proportions of low‑risk inspections are associated with lower housing values.

### 4\. How to reproduce the analysis and visualizations

To re‑run the analysis from the integrated dataset:

1. Ensure that data/processed/integrated\_food\_housing.csv has been created by the integration step.

2. Execute:  
* bash  
* python scripts/05\_data\_analysis\_visualization.py  
* or run the Snakemake workflow, which will call this script automatically.

3. Inspect the outputs in results/:  
   1. Use zip\_level\_summary.csv and risk\_by\_price\_quartiles.csv for numeric tables in the report.  
   2. Embed the PNG figures (correlation\_heatmap.png, the scatterplots, and the boxplots) as visual evidence for the relationships described in the narrative.

Because all analysis logic and plotting are scripted, someone else can regenerate the full set of tables and figures from the integrated data with a single command, ensuring reproducibility of the final analytical results.