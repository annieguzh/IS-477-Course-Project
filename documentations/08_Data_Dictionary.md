# Data Dictionary 

### 1\. Overview

This document describes the main datasets used in the project:

1. Raw Chicago Food Inspections (\`data/raw/food\_inspections.csv\`)    
2. Raw Zillow Home Value Index (ZHVI) (\`data/raw/zhvi.csv\`)    
3. Integrated establishment \- housing dataset (\`data/processed/integrated\_food\_housing.csv\`)  

Each section summarizes variable meanings and important processing decisions.

### 2\. Chicago Food Inspections (raw)

* File: \`data/raw/food\_inspections.csv\`    
* Source: City of Chicago Food Inspections API    
* Unit of analysis: One row per inspection event (multiple rows per establishment over time).

* Note: column names reflect the City of Chicago schema; only the main fields used downstream are listed here.

Identification and location: 

\- \*\*inspection\_id\*\* (string)    
  Unique ID for each inspection.

\- \*\*dba\_name\*\* (string)    
  “Doing business as” name of the establishment.

\- \*\*aka\_name\*\* (string, nullable)    
  Alternate or commonly used name.

\- \*\*license\_\*\* (string or integer)    
  Business license number. Used to help identify unique establishments.

\- \*\*facility\_type\*\* (string, nullable)    
  Category of the establishment, such as Restaurant, Grocery Store, School, etc.

\- \*\*address\*\* (string)    
  Street address of the establishment.

\- \*\*city\*\* (string)    
  City name, typically “CHICAGO”.

\- \*\*state\*\* (string)    
  Two‑letter state abbreviation, typically “IL”.

\- \*\*zip\*\* (string or integer)    
  Postal ZIP code; may appear in multiple formats (e.g., missing leading zeros, ZIP+4).

\- \*\*latitude\*\* (float, nullable)    
  Latitude coordinate for the establishment.

\- \*\*longitude\*\* (float, nullable)    
  Longitude coordinate for the establishment.

Inspection details: 

\- \*\*inspection\_date\*\* (string)    
  Date of the inspection as provided by the API (later parsed to datetime).

\- \*\*inspection\_type\*\* (string, nullable)    
  Type of inspection (e.g., Canvass, License, Complaint, Re‑inspection, etc.).

\- \*\*results\*\* (string, nullable)    
  Outcome of the inspection (e.g., Pass, Pass w/ Conditions, Fail, Out of Business).

\- \*\*risk\*\* (string, nullable)    
  City of Chicago risk classification (e.g., “Risk 1 (High)”, “Risk 2 (Medium)”, “Risk 3 (Low)”, or other/blank values).

\- \*\*violations\*\* (string, nullable)    
  Free‑text description of specific violations observed during the inspection.

\- Additional API fields (not used in the analysis) may include inspection ID variants, ward information, community area, etc.

### 3\. Zillow Home Value Index (ZHVI) (raw)

* File: \`data/raw/zhvi.csv\`    
* Source: Zillow Research ZIP‑level ZHVI CSV    
* Unit of Analysis: One row per ZIP code.

* Note: ZHVI files include metadata columns (describing the geographic region) and many date columns containing monthly ZHVI values.

Metadata columns (geography and identifiers): 

\- \*\*RegionID\*\* (integer)    
  Zillow internal identifier for the geographic region.

\- \*\*RegionName\*\* (string)    
  ZIP code for the region (later renamed to \`zip\`).

\- \*\*City\*\* (string)    
  City name associated with the ZIP code.

\- \*\*State\*\* (string)    
  Two‑letter state abbreviation.

\- \*\*Metro\*\* (string, nullable)    
  Name of the metropolitan area (e.g., “Chicago, IL”).

\- \*\*CountyName\*\* (string, nullable)    
  County name in which the ZIP code is located.

\- \*\*SizeRank\*\* or similar (integer, optional in file)    
  Rank of the region by population or housing size, if present.

Monthly ZHVI columns: 

\- \*\*YYYY-MM-DD\*\* (float, many columns)    
  Each column corresponds to a calendar month (e.g., \`2000-01-31\`, \`2000-02-29\`, …).    
  The cell value is the Zillow Home Value Index for that ZIP code and month, expressed in US dollars.

These monthly columns form a long time series per ZIP; later cleaning scripts filter ZHVI rows and derive summary statistics from them.

### 4\.  Integrated Food–Housing Dataset (processed)

* File: \`data/processed/integrated\_food\_housing.csv\`    
* Unit of Analysis: One row per unique establishment (latest inspection only) with attached ZIP‑level housing metrics from ZHVI.

This dataset is the result of:

1. Cleaning and deduplicating the food inspections data (latest inspection per establishment, valid 5‑digit ZIP codes).    
2. Cleaning the ZHVI data (removing ZIPs with excessive missing data or no recent observations).    
3. Computing summary housing metrics per ZIP (average and latest ZHVI).    
4. Inner‑joining the two cleaned datasets on 5‑digit ZIP code.

Identification and location (from food inspections): 

\- \*\*inspection\_id\*\* (string)    
  Unique ID of the inspection record representing the establishment’s latest inspection.

\- \*\*dba\_name\*\* (string)    
  Establishment’s “doing business as” name.

\- \*\*aka\_name\*\* (string, nullable)    
  Alternate or commonly used name.

\- \*\*license\_\*\* (string)    
  Business license number. Used (with address) to identify the establishment during cleaning.

\- \*\*facility\_type\*\* (string)    
  Establishment category (e.g., Restaurant, Grocery Store, School).

\- \*\*address\*\* (string)    
  Street address.

\- \*\*city\*\* (string)    
  City name as recorded in the inspection data.

\- \*\*state\*\* (string)    
  State abbreviation.

\- \*\*zip\*\* (string)    
  Cleaned 5‑digit ZIP code, used as the integration key to ZHVI.

\- \*\*latitude\*\* (float, nullable)    
  Latitude coordinate of the establishment.

\- \*\*longitude\*\* (float, nullable)    
  Longitude coordinate of the establishment.

Food safety attributes (from food inspections): 

\- \*\*inspection\_date\*\* (datetime)    
  Date of the most recent inspection for that establishment.

\- \*\*inspection\_type\*\* (string)    
  Type of the latest inspection (Canvass, License, etc.).

\- \*\*risk\*\* (string)    
  Risk classification of the establishment at the latest inspection:  
  \- \`Risk 1 (High)\`  
  \- \`Risk 2 (Medium)\`  
  \- \`Risk 3 (Low)\`

\- \*\*results\*\* (string)    
  Outcome of the latest inspection (Pass, Fail, Pass w/ Conditions, etc.).

\- \*\*violations\*\* (string, nullable)    
  Text describing violations identified during the latest inspection.

Housing attributes (from cleaned ZHVI): 

These variables summarize the ZHVI time series at the ZIP level and are constant for all establishments within the same ZIP.

\- \*\*City\*\* (string)    
  City name associated with the ZIP in the ZHVI data (often “Chicago”).

\- \*\*State\*\* (string)    
  State abbreviation in the ZHVI metadata.

\- \*\*Metro\*\* (string, nullable)    
  Metropolitan area associated with the ZIP.

\- \*\*CountyName\*\* (string, nullable)    
  County name associated with the ZIP.

\- \*\*avg\_zhvi\_all\_time\*\* (float)    
  Average ZIP‑level ZHVI across all available months in the cleaned ZHVI dataset, expressed in US dollars.

\- \*\*avg\_zhvi\_recent\*\* (float)    
  Average ZIP‑level ZHVI from January 2020 onward, capturing recent housing values.

\- \*\*zhvi\_latest\*\* (float)    
  ZHVI value for the most recent month available in the dataset, in US dollars.

### 5\. Derived ZIP‑level Analysis Table

* File: \`results/zip\_level\_summary.csv\`    
* Unit of analysis: One row per ZIP code.

This table is constructed from \`integrated\_food\_housing.csv\` and used for statistical analysis.

Risk counts and proportions: 

\- \*\*zip\*\* (string)    
  ZIP code.

\- \*\*high\_risk\_count\*\* (integer)    
  Number of inspections classified as \`Risk 1 (High)\` in that ZIP.

\- \*\*medium\_risk\_count\*\* (integer)    
  Number of inspections classified as \`Risk 2 (Medium)\` in that ZIP.

\- \*\*low\_risk\_count\*\* (integer)    
  Number of inspections classified as \`Risk 3 (Low)\` in that ZIP.

\- \*\*total\_inspections\*\* (integer)    
  Total number of inspections in that ZIP (sum of the three risk counts).

\- \*\*high\_risk\_prop\*\* (float, 0–1)    
  Fraction of inspections in that ZIP classified as \`Risk 1 (High)\`.

\- \*\*medium\_risk\_prop\*\* (float, 0–1)    
  Fraction of inspections in that ZIP classified as \`Risk 2 (Medium)\`.

\- \*\*low\_risk\_prop\*\* (float, 0–1)    
  Fraction of inspections in that ZIP classified as \`Risk 3 (Low)\`.

Attached housing metrics: 

\- \*\*avg\_zhvi\_all\_time\*\* (float)    
  Same definition as in the integrated dataset, aggregated to ZIP.

\- \*\*avg\_zhvi\_recent\*\* (float)    
  Same as above; main housing price variable used in analysis.

\- \*\*zhvi\_latest\*\* (float)    
  Most recent ZHVI value for the ZIP.

These derived variables support the correlation and visualization analyses that explore relationships between food safety risk profiles and neighborhood housing values.

