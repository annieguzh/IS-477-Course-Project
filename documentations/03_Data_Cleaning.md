# Data Quality and Cleaning Documentation

### 1\. Overview

Data quality and cleaning were handled in two dedicated scripts:

* **scripts/03\_data\_cleaning\_food.py** – profiles and cleans the Chicago food inspection data.  
* **scripts/03\_data\_cleaning\_zhvi.py** – profiles and cleans the Zillow ZHVI housing data.

Both scripts read raw CSVs from data/raw/, perform quality checks and transformations, write cleaned outputs to data/processed/, and generate SHA‑256 checksums that record the exact version of each cleaned file.

No OpenRefine was used; all profiling and cleaning operations are scripted in Python to ensure full reproducibility.

### 2\. Chicago food inspections: profiling and cleaning

Script: scripts/03\_data\_cleaning\_food.py

Input: data/raw/food\_inspections.csv  
Output: data/processed/food\_inspections\_cleaned.csv, data/processed/food\_inspections\_cleaned.sha256

Steps:

1. Load and initial profiling  
   1. The script loads the full raw inspections CSV into a pandas DataFrame.  
   2. A copy (food\_cleaned) is used for all subsequent operations to preserve the original in data/raw/.

2. Handle missing values  
   1. All rows containing any missing value are dropped with dropna().  
   2. This strict approach ensures complete records for downstream integration and analysis, and simplifies reasoning about missingness.

3. Validate and parse inspection dates  
   1. The inspection\_date column is converted to pandas datetime using pd.to\_datetime with errors="coerce".  
   2. Any rows where parsing fails (resulting in NaT) are removed with dropna(subset=\["inspection\_date"\]).  
   3. The script prints the resulting date range to confirm temporal coverage after cleaning.

4. Profile identifiers and construct a unique establishment ID  
   1. The script prints counts of unique dba\_name, license\_, and address values to understand how establishments are identified.  
   2. A composite establishment\_id is created by concatenating license\_ and address (both cast to strings, with missing values replaced by "UNKNOWN").  
   3. This ID is used to group multiple inspections belonging to the same physical establishment.

5. Keep only the latest inspection per establishment  
   1. The data is sorted by inspection\_date in descending order.  
   2. A groupby–first operation is applied on establishment\_id so that only the most recent inspection for each establishment is retained.  
   3. The helper establishment\_id column is dropped afterward.  
   4. The script prints the number of total inspection records before grouping and the number of unique establishments after, confirming that the dataset is now one row per establishment.

6. Clean ZIP codes  
   1. The zip column is cast to string and truncated to the first 5 characters (removing any ZIP+4 extensions).  
   2. Non‑numeric characters are stripped using a regular expression, leaving only digits.  
   3. Records are filtered to keep only rows where:  
      1. zip has length 5, and  
      2. zip does not start with "000".  
   4. The script reports how many records were removed due to invalid ZIP codes, the number of remaining records, and the number of unique ZIP codes, and prints a frequency sample of the most common ZIPs.

7. Column selection and final profiling  
   1. A curated set of columns is retained:  
      1. Identifiers and attributes: inspection\_id, dba\_name, aka\_name, license\_, facility\_type, address, city, state, zip  
      2. Food safety attributes: risk, inspection\_date, inspection\_type, results, violations  
      3. Location: latitude, longitude

   2. The script prints a final “cleaned data summary” including:  
      1. Total records (one per establishment).  
      2. Number of unique ZIP codes.  
      3. Final date range of inspections.  
      4. Distributions of risk, results, and top facility\_type values.  
      5. Counts of any remaining missing values by column.

8. Write cleaned file and checksum  
   1. The cleaned DataFrame is saved as data/processed/food\_inspections\_cleaned.csv.  
   2. A SHA‑256 checksum of the cleaned file is computed and written to data/processed/food\_inspections\_cleaned.sha256, documenting the exact version used for integration and analysis.

### 3\. Zillow ZHVI: profiling and cleaning

Script: scripts/03\_data\_cleaning\_zhvi.py

Input: data/raw/zhvi.csv  
Output: data/processed/zhvi\_cleaned.csv, data/processed/zhvi\_cleaned.sha256

Steps:

1. Load raw ZHVI data  
   1. The raw ZHVI CSV is read into a pandas DataFrame (zhvi), then copied to zhvi\_cleaned for cleaning.

2. Identify date and metadata columns  
   1. The script classifies columns into:  
      1. Date columns: names that contain a hyphen (-) and have length 10 (assumed YYYY-MM-DD monthly ZHVI values).  
      2. Metadata columns: all remaining columns (e.g., RegionName, City, State, Metro, CountyName).  
   2. It prints:  
      1. The number of date columns and their earliest and latest month.  
      2. The list of metadata columns.

   3. This profiling step documents the time span and structure of the ZHVI series.

3. Assess missingness across the time series  
   1. For each ZIP‑code row, the script computes missing\_per\_row as the number of missing values across all date columns.  
   2. Summary statistics (mean, median, and maximum missing months per ZIP) are printed to characterize data completeness.

4. Filter ZIP codes with excessive missing data  
   1. ZIP codes with more than 80% missing values across all months are removed.  
   2. The threshold is computed as threshold \= len(date\_columns) \* 0.8.  
   3. The script reports how many ZIPs were removed and how many remain, providing transparency on this quality filter.

5. Filter ZIP codes with no recent data  
   1. The script considers the last 12 monthly columns as the “recent” period.  
   2. For each ZIP, it computes how many of these 12 months are missing (recent\_missing).  
   3. ZIP codes with missing values in all 12 recent months (i.e., no recent data) are removed.  
   4. The number of ZIP codes removed at this stage and the number remaining are printed.

6. Final profiling  
   1. After filtering, the script prints a final summary:  
      1. Total number of ZIP codes retained.  
      2. Total number of columns.  
      3. Overall date coverage (first and last date column).  
   2. This documents the quality and temporal scope of the ZHVI dataset used in integration.

7. Write cleaned file and checksum  
   1. The cleaned ZHVI DataFrame is saved as data/processed/zhvi\_cleaned.csv.  
   2. A SHA‑256 checksum is computed and written to data/processed/zhvi\_cleaned.sha256, establishing the exact version of the cleaned housing data used later in the workflow.

### 4\. Reproducing the cleaning steps

To repeat the data quality and cleaning process on a fresh machine:

1. Run the acquisition step to populate data/raw/food\_inspections.csv and data/raw/zhvi.csv.  
2. Execute:   
   1. python scripts/03\_data\_cleaning\_food.pu  
   2. python scripts/03\_data\_cleaning\_zhvi.py  
   3. Or run the full Snakemake pipeline, which will call these scripts automatically  
3. Inspect:   
   1. data/processed/food\_inspections\_cleaned.csv and .sha256  
   2. data/processed/zhvi\_cleaned.csv and .sha256  
   3. And review the review the console output for the profiling summaries printed by each script.

Because all profiling and cleaning is scripted, these steps are fully reproducible and can be re‑run whenever the raw data updates, while still producing the same diagnostics and quality filters.