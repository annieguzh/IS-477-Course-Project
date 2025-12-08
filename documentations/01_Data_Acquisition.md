# Data Collection and Acquisition Documentation

### 1\. Overview

This project uses two primary data sources:

1. Chicago Food Inspections: Public inspection records from the City of Chicago open data API.  
2. Zillow Home Value Index (ZHVI): Public ZIP‑code–level housing value estimates from Zillow’s research site.

Because these data may change over time and cannot necessarily be redistributed in the course repository, the project includes a reproducible acquisition script and checksum files that allow anyone to re‑download the raw data and verify file integrity.

All acquisition logic is implemented in **scripts/01\_data\_acquisition.py**.

### 2\. Scripts used

File: scripts/01\_data\_acquisition.py

Responsibilities:

* Create the raw‑data directory data/raw/ if it does not exist.

* Download the complete Chicago food inspections dataset via HTTP requests to the official API and save it as data/raw/food\_inspections.csv.

* Download the ZHVI ZIP‑level CSV from Zillow and save it as data/raw/zhvi.csv.

* For each downloaded CSV, compute a SHA‑256 checksum and save it next to the data file as .sha256 (for example, data/raw/food\_inspections.sha256).

The script is written so it can be called directly:

* bash  
* python scripts/01\_data\_acquisition.py

Or indirectly through the Snakemake workflow.

### 3\. Acquisition steps: Chicago Food Inspections

1. API endpoint  
   1. The script accesses the City of Chicago’s food inspections dataset through the public SODA API endpoint:  
      1. [https://data.cityofchicago.org/resource/4ijn-s7e5.json](https://data.cityofchicago.org/resource/4ijn-s7e5.json)

      

   2. Pagination and retrieval  
      1. The API is queried in chunks of 50,000 records using $limit and $offset query parameters.  
      2. Requests are ordered by inspection\_date in descending order to ensure deterministic retrieval.  
      3. The script loops until an empty response or a partial page is returned, indicating there are no more records.  
      4. Each response is validated with resp.raise\_for\_status() to ensure HTTP errors are surfaced rather than silently ignored.  
      5. All JSON payloads are accumulated into a Python list and normalized into a single pandas DataFrame via pd.json\_normalize.

   3. Saving the raw CSV  
      1. The combined DataFrame is written to data/raw/food\_inspections.csv with index=False to preserve the original rows as‑is.  
      2. No cleaning or filtering is performed at this stage; this file represents the raw inspection data exactly as retrieved from the API.

   4. Checksum generation  
      1. After writing the CSV, the script opens the file in binary mode, computes the SHA‑256 digest with hashlib.sha256, and writes the resulting hexadecimal string to data/raw/food\_inspections.sha256.  
      2. This checksum allows any future user to verify that their downloaded file matches the original bytes used in this project.

### 4\. Acquisition steps: Zillow ZHVI

1. Download URL  
   1. The script downloads the ZHVI dataset from Zillow’s public research CSV endpoint (the URL used in this project is stored in the variable csv\_url inside the script).

2. Retrieval and saving  
   1. A single HTTP GET request is issued to the ZHVI CSV URL.  
   2. The response content is written directly to data/raw/zhvi.csv in binary mode, without modification.  
   3. As with the food inspections, this file is considered the raw, unprocessed housing data.

3. Checksum generation  
   1. The script computes a SHA‑256 hash for data/raw/zhvi.csv and writes it to data/raw/zhvi.sha256.  
   2. This checksum lets other users confirm that their copy of the ZHVI CSV matches the version used for this analysis, even if the upstream file later changes or is updated.

### 5\. How to re‑acquire the data and verify integrity

To reproduce the raw data locally:

1. Set up the project structure  
   1. Clone the repository.  
   2. Ensure the scripts/ directory (with 01\_data\_acquisition.py) exists at the project root.

2. Install dependencies  
   1. Create a Python environment with at least: requests, pandas.  
   2. Activate the environment.

3. Run the acquisition script  
   1. “Python scripts/01\_data\_acquisition.py”

4. This will:  
   1. Create data/raw/ if necessary.  
   2. Download the current versions of the Chicago food inspection data and the ZHVI CSV.  
   3. Save:  
      1. data/raw/food\_inspections.csv  
      2. data/raw/food\_inspections.sha256  
      3. data/raw/zhvi.csv  
      4. data/raw/zhvi.sha256

### 6\. Notes on redistribution

The acquisition script fetches data directly from the official providers rather than bundling the raw CSVs in the repository. This avoids licensing and size issues and ensures that others can re‑download data themselves.   
The SHA‑256 files act as a lightweight provenance mechanism: they record exactly which byte‑level versions of the source datasets were used, even if the online datasets evolve over time.

