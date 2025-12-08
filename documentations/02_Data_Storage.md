# Storage and Organization Documentation

### 1\. Overview

This project uses a simple, file‑based storage layout built around CSV files and plain‑text summaries rather than a relational database. All datasets flow through three top‑level directories:

* data/raw/ – raw source files as downloaded from external providers  
* data/processed/ – cleaned and integrated datasets used for analysis  
* results/ – derived artifacts such as summaries, figures, and analysis outputs

The script **scripts/02\_data\_storage.py** validates that the raw files exist, creates the processed and results directories if needed, and writes a human‑readable summary of the raw datasets to results/data\_storage\_summary.txt. This summary serves as lightweight documentation of the initial schema, record counts, and basic characteristics of each source.

No relational database management system is used in this project; all storage is handled via structured text files (CSV and TXT) organized in the filesystem.

### 2\. Script used for storage and organization

File: scripts/02\_data\_storage.py

Responsibilities:

1. Ensure directory structure  
   1. Defines three key paths using pathlib.Path:  
      1. RAW\_DIR \= Path("data/raw")  
      2. PROCESSED\_DIR \= Path("data/processed")  
      3. RESULTS\_DIR \= Path("results")  
   2. Creates data/processed/ and results/ with mkdir(parents=True, exist\_ok=True) so the rest of the workflow can safely write outputs there.

2. Load raw datasets  
   1. Reads the raw Chicago food inspections CSV:  
      1. data/raw/food\_inspections.csv  
   2. Reads the raw ZHVI CSV:  
      1. data/raw/zhvi.csv  
   3. These files are produced by the acquisition script and remain unmodified here; they are loaded only to introspect structure and basic statistics.

3. Generate a storage summary report  
   1. Builds a list of text lines describing:  
      1. The filesystem layout, including the roles of data/raw/, data/processed/, and results/.  
      2. Naming conventions:  
         1. Raw files: data/raw/\<dataset\_name\>.csv  
         2. Processed files: data/processed/\<dataset\_name\>\_cleaned.csv or data/processed/integrated\_\*.csv  
         3. Checksums: .sha256 files stored next to their corresponding CSVs  
         4. Results: results/\*.csv, results/\*.txt, results/\*.png

   2. For the food inspections file, the script records:  
      1. Total number of records (len(chicago\_food\_inspection))  
      2. Number of columns and the full column name list  
      3. Number of unique ZIP codes if a zip column is present

   3. For the ZHVI file, the script records:  
      1. Total number of records (len(zhvi))  
      2. If a City column exists, the top 5 cities by record count and the number of rows where City \== "Chicago".

4. Write the summary to disk  
   1. All collected lines are written to results/data\_storage\_summary.txt.  
   2. The same text is printed to standard output when the script is run, so users can see the summary in the console.

The script is designed to be run directly:

* bash  
* python scripts/02\_data\_storage.py

or indirectly as part of the automated workflow.

### 3\. Filesystem structure and naming conventions

After running the acquisition and storage steps, the project directories are organized as follows:

* data/raw/  
  * Contains unmodified source data as downloaded:  
    * food\_inspections.csv – full Chicago food inspections dataset.  
    * food\_inspections.sha256 – SHA‑256 checksum for the inspections CSV.  
    * zhvi.csv – ZHVI ZIP‑level housing values.  
    * zhvi.sha256 – SHA‑256 checksum for the ZHVI CSV.  
  * These files represent the canonical raw inputs and are never overwritten by cleaning or analysis code.

* data/processed/  
  * Created by later stages of the pipeline (cleaning, integration).  
  * Contains:  
    * Cleaned datasets, e.g. food\_inspections\_cleaned.csv, zhvi\_cleaned.csv.  
    * Integrated datasets, e.g. integrated\_food\_housing.csv.  
    * Matching checksum files (e.g. food\_inspections\_cleaned.sha256), which document the exact byte‑level version of each processed file.

* results/  
  * Contains human‑readable summaries and analysis outputs:  
    * data\_storage\_summary.txt – text report produced by 02\_data\_storage.py, documenting the storage layout and basic properties of the raw datasets.  
    * Other downstream results such as integrated\_data\_summary.txt, zip\_level\_summary.csv, analysis text outputs, and generated figures (PNG).

Naming conventions used throughout the project:

* Raw source files: data/raw/\<dataset\>.csv plus \<dataset\>.sha256.

* Cleaned files: data/processed/\<dataset\>\_cleaned.csv (+ .sha256).

* Integrated analysis datasets: data/processed/integrated\_\<description\>.csv (+ .sha256).

* Result artifacts: results/\<description\>.(csv|txt|png).

This consistent layout makes it clear where each dataset comes from and which transformation stage it represents. It also allows the automated workflow to target specific files (for example, Snakemake rules can declare data/raw/\*.csv as inputs and data/processed/\*.csv as outputs) without ambiguity.

### 4\. How someone else would use this structure

To understand or extend the project, a new user should:

1. Run the acquisition script to populate data/raw/.  
2. Run scripts/02\_data\_storage.py (or the full Snakemake pipeline) to create data/processed/, results/, and the results/data\_storage\_summary.txt report.  
3. Use the directory layout and naming conventions described above to locate any dataset:  
   1. Start from raw inputs in data/raw/.  
   2. Follow the processing chain through data/processed/.  
   3. Consult results/ for human‑readable descriptions and visualizations associated with each step.

Because all intermediate and final datasets are written to clearly named CSV and TXT files under these directories, the storage and organization layer forms a transparent provenance chain from raw acquisition to final analysis.

