# Data Integration Documentation

### 1\. Overview

The goal of data integration in this project is to combine establishment‑level food inspection records from the City of Chicago with ZIP‑code-level housing value estimates from the Zillow Home Value Index (ZHVI). The integration is implemented in a dedicated Python script that reads the cleaned inputs, constructs ZIP‑level housing metrics, merges the datasets on ZIP code, and writes both a machine‑readable integrated table and a human‑readable summary.

The resulting integrated dataset contains one row per food establishment (latest inspection only), enriched with several housing value statistics for the ZIP code where the establishment is located.

### 2\. Scripts used

Data integration is handled entirely in:

* **scripts/04\_data\_integration.py**

This script:

* Reads the cleaned food inspections data (food\_inspections\_cleaned.csv) and cleaned ZHVI data (zhvi\_cleaned.csv) from data/processed/.

* Prepares the ZHVI dataset by renaming and standardizing the ZIP column and computing summary housing metrics.

* Performs the join on ZIP code and profiles the resulting integrated dataset.

* Writes the integrated CSV and a text summary of the integration process to disk, as well as a SHA‑256 checksum of the integrated file.

Users can inspect the exact implementation details by opening the script.

### 3\. Conceptual model and integration schema

Entities

1. Food establishments  
   1. Unit of analysis: one record per establishment, corresponding to its most recent inspection.  
   2. Key attributes:  
      1. Business identifiers (inspection\_id, dba\_name, aka\_name, license\_).  
      2. Location (address, city, state, zip, latitude, longitude).  
      3. Food safety attributes (risk, inspection\_date, inspection\_type, results, violations).

2. Housing markets (ZIP‑code–level ZHVI)  
   1. Unit of analysis: one record per ZIP code.  
   2. Key attributes:  
      1. Geographic identifiers (RegionName / zip, City, State, Metro, CountyName).  
      2. Monthly ZHVI values across many years.  
      3. Derived summary metrics (see below).

Integration key and relationship

* Integration key: 5‑digit ZIP code stored as a string in both datasets.

* Relationship: many‑to‑one. Multiple establishments in the same ZIP code are associated with the same set of ZHVI housing metrics.

* Join type: inner join on ZIP code, so only ZIPs present in both datasets are retained. This ensures that every establishment in the integrated dataset has corresponding housing information.

Integrated schema

The integrated dataset integrated\_food\_housing.csv combines:

* All analysis‑relevant columns from the cleaned food inspections table, including identifiers, facility type, risk category, inspection results, address, and coordinates.

* Selected columns from the ZHVI table:  
  * zip, City, State, Metro, CountyName.  
  * avg\_zhvi\_all\_time: average ZHVI across all available months for that ZIP.  
  * avg\_zhvi\_recent: average ZHVI for recent years (from January 2020 onward), capturing current market conditions.  
  * zhvi\_latest: the ZHVI value for the most recent month in the dataset.

Each row therefore describes an individual food establishment and the housing market characteristics of its surrounding ZIP code.

### 4\. Integration steps

The integration process consists of the following stages:

1. Load cleaned inputs  
   1. The script reads the cleaned food and housing datasets from data/processed/. These inputs have already been de‑duplicated, validated, and filtered for data quality in the earlier cleaning stage.

2. Standardize ZIP columns  
   1. To ensure the join key is consistent across sources:  
      1. The ZHVI ZIP identifier (RegionName) is renamed to zip.  
      2. The zip column in both dataframes is cast to string format, matching the five‑digit ZIP codes produced during cleaning.

3. Identify ZHVI date columns and compute summary metrics  
   1. The script distinguishes:  
      1. Date columns: monthly ZHVI values, identified by their YYYY-MM-DD style names.  
      2. Metadata columns: non‑date attributes such as ZIP identifiers and geographic information.  
   2. Using the date columns, it computes three ZIP‑level housing metrics:  
      1. avg\_zhvi\_all\_time: the mean of all available monthly ZHVI values for each ZIP, providing a long‑run average.  
      2. avg\_zhvi\_recent: the mean of monthly values from January 2020 onward, capturing recent housing conditions more relevant to current food inspections.  
      3. zhvi\_latest: the ZHVI value in the most recent month available in the file, providing a current point estimate.

   3. Only these summary metrics and a small set of geographic attributes are kept for integration, which reduces the dimensionality of the ZHVI dataset while preserving the key information needed for the analysis.

4. Check ZIP overlap  
   1. Before performing the join, the script:  
      1. Collects the set of ZIP codes present in the food inspection dataset.  
      2. Collects the set of ZIP codes present in the ZHVI subset used for merging.  
      3. Computes and logs:  
         1. The number of food ZIPs.  
         2. The number of housing ZIPs.  
         3. The size of the intersection (ZIPs present in both).  
         4. Counts of ZIPs present only in food or only in housing.  
   2. These statistics are written into results/integrated\_data\_summary.txt to document which portions of each dataset participate in the integrated analysis.

5. Inner join on ZIP  
   1. The core integration step is a ZIP‑based inner join:  
      1. Only records with ZIP codes present in both datasets are kept.  
      2. For each food establishment, the corresponding ZHVI metrics of its ZIP are attached.  
      3. This design avoids missing values in the housing variables at the cost of discarding establishments in ZIPs without ZHVI coverage.

6. Post‑integration profiling  
   1. After merging, the script performs basic diagnostics:  
      1. Counts total integrated records (establishments) and unique ZIP codes.  
      2. Reports the number of columns in the integrated dataset.  
      3. Computes the distribution of establishments per ZIP (mean, median, minimum, maximum).  
      4. Displays the distribution of risk categories.  
      5. Summarizes zhvi\_latest with mean, median, minimum, and maximum values.  
      6. Lists the top five facility\_type values.  
   2. These results are printed and saved in the integration summary file so that users can understand the size and composition of the integrated table without opening the CSV.

7. Write integrated dataset and checksum  
   1. The integrated dataset is written to data/processed/integrated\_food\_housing.csv.  
   2. A SHA‑256 checksum of this file is computed and stored as data/processed/integrated\_food\_housing.sha256, recording the exact bytes used for analysis and supporting reproducibility and integrity checks.  
   3. The accumulated log messages are written to results/integrated\_data\_summary.txt, which documents the integration steps, overlap statistics, and profiling results.

### 5\. Reproducing the integration

To regenerate the integrated dataset:

1. Run the acquisition and cleaning scripts (or execute the full Snakemake workflow) to produce the cleaned inputs in data/processed/.

2. Execute the integration script:

* bash  
  python scripts/04\_data\_integration.py  
    
    
3. Inspect:

* data/processed/integrated\_food\_housing.csv – establishment‑level data with housing metrics.

* data/processed/integrated\_food\_housing.sha256 – checksum for integrity verification.

* results/integrated\_data\_summary.txt – documentation of which ZIPs were used and how the datasets were combined.

This provides a transparent and fully reproducible path from cleaned inputs to the integrated dataset used in the final analysis.