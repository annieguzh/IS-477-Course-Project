# Workflow Automation and Provenance Documentation

**Tools**: Snakemake, Python scripts, SHA‑256 checksums.

### 1\. Script modularization

The original exploratory workflow in workflow.ipynb was refactored into five standalone Python scripts, each responsible for one stage of the pipeline:

* scripts/01\_data\_acquisition.py  
  * Downloads Chicago food inspections via the official API and the ZHVI CSV from Zillow.  
  * Saves raw files in data/raw/ and writes matching .sha256 checksum files for provenance.

* scripts/02\_data\_storage.py  
  * Ensures data/processed/ and results/ exist.  
  * Reads the raw CSVs and writes results/data\_storage\_summary.txt, documenting directory layout, file naming conventions, and basic dataset characteristics.

* scripts/03\_data\_cleaning\_food.py  
  * Cleans the food inspection data: drops missing values, parses inspection\_date, keeps only the latest inspection per establishment, standardizes and validates ZIP codes, and writes data/processed/food\_inspections\_cleaned.csv plus a checksum.

* scripts/03\_data\_cleaning\_zhvi.py  
  * Cleans the ZHVI data: identifies date columns, removes ZIP codes with excessive missing or stale data, and writes data/processed/zhvi\_cleaned.csv plus a checksum.

* scripts/04\_data\_integration.py  
  * Renames RegionName to zip, computes ZIP‑level ZHVI summaries (avg\_zhvi\_all\_time, avg\_zhvi\_recent, zhvi\_latest), and performs an inner join with the cleaned food inspections on zip.  
  * Writes data/processed/integrated\_food\_housing.csv, data/processed/integrated\_food\_housing.sha256, and a human‑readable integration report in results/integrated\_data\_summary.txt.

* scripts/05\_data\_analysis\_visualization.py  
  * Aggregates to ZIP level, computes risk proportions, and merges with ZHVI values.  
  * Saves the ZIP‑level table (results/zip\_level\_summary.csv).  
  * Produces all figures used in the report (correlation\_heatmap.png, scatterplots, boxplots) and numeric summaries (risk\_correlations.txt, risk\_by\_price\_quartiles.csv).

Each script can be executed independently, and all intermediate datasets are written to disk, which provides transparent provenance between steps.

### 2\. Snakemake workflow

The Snakefile encodes the dependencies between stages as rules:

* data\_acquisition \-\> creates raw inputs in data/raw/.

* data\_storage \-\> summarizes storage and organization, consuming the raw files.

* clean\_food and clean\_zhvi \-\> consume the raw files and produce cleaned datasets.

* integrate\_data \-\> consumes cleaned datasets and produces the integrated CSV plus an integration summary.

* analyze\_visualize \-\> consumes the integrated CSV and produces all final tables and figures in results/.

* Run\_all \-\> declares all final result files as its input. Running:  
  * Bash  
    snakemake \--cores 1  
  * (or the notebook cell \! snakemake \--cores 1\) triggers Snakemake to:  
    * Check which target files are missing or outdated.  
  * Automatically run the required rules in the correct order, starting from data\_acquisition and ending with analyze\_visualize.

Reuse existing intermediate files where possible, ensuring efficient, incremental recomputation.

This DAG encodes the provenance of every artifact: for each figure or summary file in results/, one can trace back which script, which inputs, and which external data sources produced it.

### 3\. Run‑all script

To make reproduction trivial, a small “run all” script is provided. In notebook form:

python  
\# Run\_All\_Script\_Snakemake.ipynb  
\! snakemake \--cores 1 \--delete-all-output  
\! snakemake \--cores 1

This notebook:

* Deletes all outputs managed by Snakemake, ensuring a clean state.  
* Rebuilds the entire analysis pipeline from scratch, from downloading the data to regenerating all final plots and tables.

On the command line, the same can be done with a shell script:

bash  
\#\!/usr/bin/env bash  
set \-e  
snakemake \--cores 1 \--delete-all-output  
snakemake \--cores 1

### 4\. Steps to repeat the workflow

To fully reproduce the project on a fresh machine:

1) Clone the repository and create the expected directory tree:  
   1) data/raw/, data/processed/, results/, scripts/.

2) Create and activate the project environment (e.g., using conda or pip) with the required Python packages: pandas, requests, numpy, matplotlib, seaborn, scipy, statsmodels, snakemake.

3) Run:  
   1) bash  
      snakemake \--cores 1  
   2) or open Run\_All\_Script\_Snakemake.ipynb and run all cells.

4) Inspect outputs:  
   1) Cleaned and integrated data in data/processed/.  
   2) Checksums documenting file integrity.  
   3) Storage and integration summaries in results/\*.txt.  
   4) Final analysis tables and visualizations in results/\*.csv and results/\*.png.

This combination of modular scripts, Snakemake rules, and a run‑all entry point provides an automated, reproducible workflow that captures the full lifecycle of our project – from raw data acquisition through cleaning, integration, analysis, and visualization.