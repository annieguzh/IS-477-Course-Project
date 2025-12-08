# Reproducibility and Transparency Package

### 1\. How to reproduce the analysis

To fully reproduce this project from scratch on a new machine:

1. Clone the repository  
   1. Clone the project GitHub repository to a local directory of your choice.  
   2. The repo contains all Python scripts (scripts/), the Snakefile, documentation (docs/), and example notebooks.

2. Set up the Python environment  
   1. Create a virtual environment (e.g., with conda or python \-m venv).  
   2. Install dependencies using:  
      1. bash  
      2. pip install \-r requirements.txt  
   3. The requirements.txt file lists all required packages, and a separate pip\_freeze.txt (or similar) records the exact versions used when the project was run, so the environment can be closely matched.

3. Acquire data  
   1. The raw data is not committed to the repository; instead, it is retrieved programmatically.  
   2. Run either:  
      1. The Snakemake workflow (recommended):  
         1. Bash  
         2. snakemake \--cores 1 data/raw/food\_inspections.csv data/raw/zhvi.csv  
         3. or simply snakemake \--cores 1, which will also run downstream steps.  
      2. Or, call the acquisition script directly:  
         1. python scripts/01\_data\_acquisition.py  
   3. This downloads:  
      1. Chicago food inspections from the City of Chicago open data API into data/raw/food\_inspections.csv.  
      2. ZIP‑level ZHVI from Zillow into data/raw/zhvi.csv.

   4. Matching .sha256 checksum files are written next to each raw CSV for integrity verification.

4. Run the full workflow  
   1. From the project root, run:  
      1. snakemake \--cores 1  
   2. Snakemake will orchestrate the entire pipeline:  
      1. scripts/01\_data\_acquisition.py (data collection)  
      2. scripts/02\_data\_storage.py (storage summary)  
      3. scripts/03\_data\_cleaning\_food.py and scripts/03\_data\_cleaning\_zhvi.py (cleaning and quality checks)  
      4. scripts/04\_data\_integration.py (ZIP‑level integration)  
      5. scripts/05\_data\_analysis\_visualization.py (analysis and figures)

   3. Alternatively, each script can be run manually in order if Snakemake is not available.

5. Inspect outputs  
   1. Processed data (cleaned and integrated):  
      1. data/processed/food\_inspections\_cleaned.csv  
      2. data/processed/zhvi\_cleaned.csv  
      3. data/processed/integrated\_food\_housing.csv  
      4. Each has a corresponding .sha256 checksum file documenting the exact version analyzed.

   2. Results and figures:  
      1. Text summaries and numeric outputs in results/:  
         1. Data\_storage\_summary.txt  
         2. Integrated\_data\_summary.txt  
         3. Zip\_level\_summary.csv  
         4. Risk\_correlations.txt  
         5. risk\_by\_price\_quartiles.csv  
      2. Visualizations in results/:  
         1. Correlation\_heatmap.png  
         2. High\_risk\_vs\_zhvi\_scatter.png  
         3. Low\_risk\_vs\_zhvi\_scatter.png  
         4. Housing\_by\_high\_risk\_tertiles.png  
         5. housing\_by\_low\_risk\_tertiles.png

   3. These files constitute the “actual results” referenced and are sufficient to regenerate the tables and figures in the report.

### 2\. Data access via Box

Because the raw and processed datasets are too large and may change over time, a snapshot of the key output data is archived on Box.

* A shareable Box folder link is provided in the written report.

* The Box folder contains:  
  * data/processed/food\_inspections\_cleaned.csv  
  * data/processed/zhvi\_cleaned.csv  
  * data/processed/integrated\_food\_housing.csv  
  * The corresponding .sha256 files  
  * All files currently in the local results/ directory (tables and figures)

Instructions for TAs or other users:

1. Download the entire Box folder.

2. Place the data/processed/ subfolder from Box into the project’s data/ directory, preserving the path structure:  
   1. \<project\_root\>/data/processed/...

3. Place the results/ subfolder from Box directly under \<project\_root\>/results/ if you want pre‑computed outputs without re‑running the pipeline.

To prevent large data files from being tracked in Git, the specific Box‑backed directories (e.g., data/processed/, results/) are listed in .gitignore so that only code and small metadata files are version‑controlled.

### 3\. Software dependencies

The repository includes:

* requirements.txt – a minimal specification of the packages needed to run the project (for example: pandas, numpy, requests, matplotlib, seaborn, scipy, statsmodels, snakemake).

* pip\_freeze.txt (or similarly named file) – the exact output of pip freeze from the environment used to generate the submitted results. This allows others to recreate the same environment if needed.

Recommended reproduction procedure:

1. Create a fresh environment.

2. Install dependencies using requirements.txt.

3. If precise replication of versions is necessary, install packages using the pinned versions in pip\_freeze.txt instead.

### 4\. Summary

In combination, the following elements make the project reproducible and transparent:

* Programmatic data acquisition with checksums.

* Clear directory structure for raw, processed, and result data.

* Modular Python scripts plus a Snakemake workflow that automates the full pipeline.

* Archived copies of processed data and results on Box, with instructions on where to place them in the project tree.

* Explicit dependency specification via requirements.txt and recorded package versions via pip freeze.

With this information, another researcher can reconstruct the environment, re‑acquire the data, re‑run all processing steps, and regenerate the analysis outputs used in the final report.