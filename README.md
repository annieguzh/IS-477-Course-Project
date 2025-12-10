# Chicago Food Safety Risk and Neighborhood Housing Values

## Contributor: 

* ## Annie Gu

* ## Judy Zhang

Contribution statement: This project is a collaborative effort by Annie Gu and Judy Zhang. Both team members contributed to the design, implementation, and documentation of the work. 

# 1\. Summary

This project investigates how food safety risk levels of restaurants and other food establishments in Chicago relate to neighborhood housing prices at the ZIP-code level. The focus is not only on the substantive question \- whether areas with more “high-risk” or “low-risk” inspections have different housing values \- but also on implementing a fully reproducible, automated data pipeline.

Motivated by urban inequality and environmental justice questions, we ask two main research questions. First, does the proportion of low-risk versus high-risk food establishments in a ZIP code correlate with local housing prices? Second, are there particular parts of Chicago where this relationship appears stronger or weaker? These questions matter because food safety and housing markets are both linked to neighborhood socioeconomic conditions: violations may cluster in economically disadvantaged areas, while higher housing values may reflect stronger consumer demand for safer environments.

Two primary datasets are used. Chicago food inspection data are retrieved programmatically from the City of Chicago open data API. These records describe individual inspections, including risk category, results, violation details, and establishment location. Zillow Home Value Index (ZHVI) data provide monthly ZIP-level housing value estimates for the United States. These are downloaded as CSV from the Zillow Research website. Both datasets are stored locally under \`data/raw/\` and are not committed to the repository (but can be accessed through Box at [https://uofi.box.com/s/gd6l8kv3m0cak50shb8uufv0q7vn0x6n](https://uofi.box.com/s/gd6l8kv3m0cak50shb8uufv0q7vn0x6n)).

For each ZIP code, we compute the proportion of restaurants and other food establishments classified as “high-risk,” “medium-risk,” or “low-risk” based on their most recent inspection. We then integrate these risk indicators with typical home value index (ZHVI) estimates from Zillow to explore whether neighborhoods with different food safety records also tend to have different property values.

To answer our research questions, we design a fully reproducible pipeline. The project workflow is implemented as a set of modular Python scripts under \`scripts/\` orchestrated by a Snakemake pipeline (\`Snakefile\`). The pipeline automates the entire process from data acquisition, storage and organization, cleaning, and integration to the final analysis and visualization. The main entry point is the Snakemake “run all” target, which can rebuild all processed data and results from scratch.

Substantively, the integrated dataset captures one row per establishment (latest inspection only), linked to ZIP-level housing metrics derived from ZHVI, including long-run average, recent average, and most recent housing values. Analysis aggregates inspections to the ZIP level, computing the proportions of high-, medium-, and low-risk inspections per ZIP and correlating these proportions with housing values. Visualizations include correlation heatmaps, scatterplots with regression lines, and boxplots comparing housing values across ZIPs grouped by risk share.

Our main findings are somewhat counterintuitive: ZIP codes with higher proportions of inspections classified as “Risk 1 (High)” tend to have higher housing values, whereas ZIPs with higher proportions of “Risk 3 (Low)” inspections tend to have lower housing values. The relationships are moderately strong and statistically significant at the ZIP level. However, our analysis is intentionally descriptive and exploratory. We rely on observational data at the ZIP level, and we do not claim any causal relationship between housing prices and food safety risks. In the Future Work section, we outline how more granular data and stronger modeling techniques could be used to probe alternative explanations.

# 2\. Data profile

## 2.1 City of Chicago Food Inspections

The first dataset is the City of Chicago Food Inspections dataset, accessed programmatically via the official open-data API. The dataset can be located here: [https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about\_data](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about_data). The acquisition script paginates through the API endpoint, retrieving all available records and writing them to `data/raw/food_inspections.csv` along with a SHA-256 checksum file for provenance **(**please see acquisition script: [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/01\_data\_acquisition.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/01_data_acquisition.py) and documentation: [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/01\_Data\_Acquisition.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/01_Data_Acquisition.md) referenced here**)**. According to our storage summary, the raw file contains 301,259 inspection records across 131 ZIP codes within Chicago.

Each record corresponds to a single inspection of a specific establishment. Key fields used in our project include establishment name (`dba_name`), license number, address, ZIP code, facility type (e.g., restaurant, grocery, school), inspection date, risk category (High, Medium, Low), and inspection result (e.g., Pass, Fail, Pass with Conditions). These attributes allow us to profile establishments, group inspections by ZIP code, and compare risk distributions across neighborhoods.

Ethically, this dataset is suitable for our project because it does not contain personally identifiable information about customers. The data focuses on businesses and is published by the city as public information. Our analysis stays at the establishment and ZIP-code level and does not attempt to single out individual inspectors or staff. Nevertheless, we are careful not to interpret violations as evidence about individual workers; instead, we treat risk levels as indicators of broader regulatory and infrastructure conditions.

## 2.2 Zillow Home Value Index (ZHVI)

The second dataset is the Zillow Home Value Index (ZHVI), obtained from Zillow Research as a CSV file. We obtained the dataset through this link: [https://www.zillow.com/research/data/](https://www.zillow.com/research/data/) (under Home Value, select “Zip Code” for Geography). This dataset provides time-series estimates of typical home values at various geographic levels, including ZIP code. Our acquisition script downloads the CSV into `data/raw/zhvi.csv` and computes a matching SHA-256 checksum (please see acquisition script [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/01\_data\_acquisition.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/01_data_acquisition.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/01\_Data\_Acquisition.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/01_Data_Acquisition.md) referenced here). The raw file contains 26,309 rows in total, of which 56 correspond to Chicago ZIP codes.

For each ZIP code, the ZHVI file includes metadata columns such as region name, city, state, and county, followed by monthly ZHVI values from January 2000 through October 2025\. In our project, we focus on ZIP codes in the city of Chicago and construct three summary measures: an all-time average ZHVI, a recent-period average (using all ZHVI observations from 2020 onward), and the latest available ZHVI value. These variables allow us to compare long-run and recent housing price levels across ZIP codes.

Zillow Research explicitly states that the data is provided for academic and non-commercial use with attribution, and that derivative products must reference Zillow (as summarized in our project plan). In our report, we follow these terms by citing Zillow as the source for all home-value statistics and by using the data purely for an academic class project.

## 2.3 Integrated dataset and storage layout

After cleaning, we produce three key processed datasets stored under `data/processed/`:

* `food_inspections_cleaned.csv` – one record per establishment with its latest inspection and risk level.

* `zhvi_cleaned.csv` – Chicago ZIP codes with selected ZHVI columns.

* `integrated_food_housing.csv` – the result of merging the first two datasets by ZIP code.

Each processed CSV has a matching `.sha256` file. A separate storage-summary script writes `results/data_storage_summary.txt`, which documents the directory structure, file sizes, row counts, and basic profiling statistics (please see storage documentation referenced here [https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/data\_storage\_summary.txt](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/data_storage_summary.txt)). For long-term preservation, we also upload the processed datasets and selected results to a Box folder with a shared link that can be placed in the report **(**please see Box folder link referenced here [https://uofi.box.com/s/iqb8b20vqd2oecxt4m4evjnwikd1ad2s](https://uofi.box.com/s/iqb8b20vqd2oecxt4m4evjnwikd1ad2s)).

We also have data storage script [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/02\_data\_storage.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/02_data_storage.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/02\_Data\_Storage.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/02_Data_Storage.md) that can be accessed here. 

# 3\. Data quality

## 3.1 Food inspections cleaning and profiling

The food inspection cleaning script performs several steps to address missing values, inconsistent types, and duplicate records (please see cleaning script [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/03\_data\_cleaning\_food.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/03_data_cleaning_food.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/03\_Data\_Cleaning.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/03_Data_Cleaning.md) referenced here). 

First, the script reads the raw CSV and drops rows that are entirely empty or missing key fields. Inspection dates are parsed to proper datetime objects; any rows with unparseable dates are removed. This ensures that we can reliably identify the most recent inspection per establishment and compute date ranges.

Next, the script constructs a composite `establishment_id` by concatenating license number, postal address, and DBA name. Using this ID, we sort all inspections by date in descending order and keep only the first record for each establishment. This reduces repeated inspections and aligns the dataset with our research question, which focuses on the current risk status of each location. After this step, we end up with one row per establishment instead of multiple historical inspections.

ZIP codes require special treatment. In the raw file, some ZIP codes are missing or include extra characters. The cleaning script standardizes ZIP codes to five-digit strings, strips non-numeric characters, and filters out values that are not valid Chicago ZIP codes (e.g., those starting with “000”). This procedure removes a small number of records with unusable location information. While this introduces a slight bias toward better-documented establishments, it is necessary to perform ZIP-level analysis.

The cleaning script prints distributions of risk categories, inspection outcomes, and facility types. In the cleaned dataset, the majority of establishments are classified as “High Risk,” followed by “Medium” and a smaller number of “Low” risk cases. Restaurants and grocery stores constitute the largest facility types. We keep these distributions in mind when interpreting later results, because a heavy concentration of high-risk classifications may reflect inspection policy or coding practices rather than inherently unsafe establishments.

## 3.2 ZHVI cleaning and filtering

For the ZHVI dataset, the main quality issues are temporal completeness and handling missing values. We first profile the raw file and confirm that it contains 26,309 rows in total, of which 56 correspond to ZIP codes in the city of Chicago, as reported in `data_storage_summary.txt`.

The ZHVI cleaning script then focuses on the time-series structure and missingness pattern (please see ZHVI cleaning script [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/03\_data\_cleaning\_zhvi.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/03_data_cleaning_zhvi.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/03\_Data\_Cleaning.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/03_Data_Cleaning.md) referenced here). It identifies all date columns, reports the overall coverage from 2000-01-31 to 2025-10-31, and removes ZIP codes with more than 80% missing ZHVI values. It also drops ZIP codes that have no data in the most recent 12 months so that the resulting averages remain meaningful. Alignment between ZHVI ZIP codes and food-inspection ZIP codes is checked later in the integration script, which reports that 58 ZIP codes appear in both datasets and discards ZIPs that appear in only one dataset.

The script calculates summary statistics for the cleaned ZHVI subset and reports the number of remaining ZIP codes. Because ZHVI is an aggregate index, we do not have access to individual transactions; this limits our ability to assess outliers or data entry errors directly. Instead, we rely on sanity checks—such as ensuring that values are positive and that recent values generally exceed early-2000 levels—to identify any obviously incorrect rows. No such major anomalies were found for the ZIP codes that survive our cleaning and integration steps.

## 3.3 Integration quality and coverage

The integration script merges the cleaned inspection and ZHVI datasets on the standardized five-digit ZIP code. Before merging, it computes a ZIP overlap report: there are 59 ZIP codes in the cleaned food inspections, 24,745 ZIP codes in the full ZHVI file, and 58 ZIP codes appearing in both. Only one food ZIP lacks a corresponding ZHVI record; conversely, many ZHVI ZIPs fall outside Chicago’s food inspection coverage. We use an inner join so that the final integrated dataset includes only the 58 ZIP codes with both food inspections and ZHVI values (please see integration script [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/04\_data\_integration.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/04_data_integration.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/04\_Data\_Integration.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/04_Data_Integration.md) referenced here).

Post-integration profiling shows that the final dataset has 17,366 establishments and 58 unique ZIP codes. The number of establishments per ZIP ranges from 14 to 783, with a median of about 285\. This uneven coverage is an important caveat: risk proportions in ZIP codes with very few establishments may be noisy. In our later analysis we keep this limitation in mind, and the visualization of total inspections by ZIP helps identify sparsely covered areas.

# 

# 4\. Findings

The script used for our findings for the project can be accessed [https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/05\_data\_analysis\_visualization.py](https://github.com/annieguzh/IS-477-Course-Project/blob/main/scripts/05_data_analysis_visualization.py) and documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/05\_Data\_Analysis\_Visualization.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/05_Data_Analysis_Visualization.md). 

## 4.1 ZIP-level risk distributions

Using the integrated dataset, the analysis script aggregates establishments by ZIP code and counts the number of high-, medium-, and low-risk establishments in each area. It then computes the corresponding proportions and writes them, along with housing metrics, to `results/zip_level_summary.csv`. Across the 58 ZIP codes, the average high-risk proportion is about 0.72, with values ranging from approximately 0.47 to 0.87. Low-risk proportions are generally much smaller, with a mean around 0.08.

This distribution shows that, according to the city’s classification scheme, most inspected establishments are considered high risk. As noted earlier, this does not necessarily mean that they are performing poorly; instead, many restaurants are inherently classified as high risk due to the types of food they handle. Nonetheless, the variation across ZIP codes in the fraction of low-risk establishments provides a useful signal about differences in local inspection outcomes.

## 4.2 Comparing housing-price quartiles

To explore how risk proportions vary with housing prices, we stratify ZIP codes into quartiles based on their recent average ZHVI values (`avg_zhvi_recent`) and compute average risk proportions within each group. The resulting summary is stored in `results/risk_by_price_quartiles.csv` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/risk\_by\_price\_quartiles.csv](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/risk_by_price_quartiles.csv)). In the lowest-price quartile (Q1), the average high-risk proportion is about 0.63, while the average low-risk proportion is about 0.13. In the highest-price quartile (Q4), the average high-risk proportion rises to roughly 0.81, and the low-risk proportion falls to around 0.05.

Boxplots in `housing_by_high_risk_tertiles.png` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/housing\_by\_high\_risk\_tertiles.png](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/housing_by_high_risk_tertiles.png))  and `housing_by_low_risk_tertiles.png` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/housing\_by\_low\_risk\_tertiles.png](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/housing_by_low_risk_tertiles.png)) visualize these patterns more directly. When we group ZIP codes by high-risk proportion tertiles, we see that the tertile with the highest fraction of high-risk establishments tends to have the highest median ZHVI values. Conversely, when grouping by low-risk tertiles, the tertile with the highest fraction of low-risk establishments tends to have noticeably lower housing prices. Individual points overlaid on the boxplots show that this pattern holds for most ZIP codes, not just a few outliers.

## 4.3 Correlations between risk and housing values

The scatterplots `high_risk_vs_zhvi_scatter.png` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/high\_risk\_vs\_zhvi\_scatter.png](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/high_risk_vs_zhvi_scatter.png)) and `low_risk_vs_zhvi_scatter.png` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/low\_risk\_vs\_zhvi\_scatter.png](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/low_risk_vs_zhvi_scatter.png)) summarize the relationship between risk proportions and recent average ZHVI at the ZIP level. In the high-risk scatterplot, points trend upward: ZIP codes with higher high-risk proportions tend to have higher recent ZHVI values. In the low-risk scatterplot, the trend is negative: areas with more low-risk establishments tend to have lower recent housing prices.

These visual impressions are confirmed by the correlation heatmap `correlation_heatmap.png` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/correlation\_heatmap.png](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/correlation_heatmap.png)) and the corresponding text file `risk_correlations.txt` ([https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/risk\_correlations.txt](https://github.com/annieguzh/IS-477-Course-Project/blob/main/results/risk_correlations.txt)). Using Pearson correlations, we find r \= 0.626 between high-risk proportion and recent average ZHVI, r \= −0.546 for low-risk proportion, and r \= −0.537 for medium-risk proportion. While correlation coefficients are limited by the small number of ZIP codes (58), their magnitude suggests a fairly strong relationship: in our sample, higher housing prices are associated with higher shares of establishments classified as high risk.

One possible interpretation is that high-value neighborhoods contain many restaurants and complex food businesses that are inherently categorized as high risk (for example, because of menu complexity, cooking methods, or volume), while lower-value neighborhoods may have more small groceries and simple establishments that qualify as low risk. Our observational data cannot distinguish between these mechanisms, but the pattern cautions against assuming that “expensive neighborhoods” automatically provide safer food environments.

# 

# 5\. Future work

Our analysis is intentionally descriptive and limited to ZIP-level aggregates. Several extensions could strengthen the conclusions and address current limitations. First, a more nuanced risk metric could distinguish between “inherent” risk categories assigned by regulation and actual inspection outcomes, such as the number and severity of violations. Incorporating violation counts or scores might reveal whether high-value neighborhoods have different types of issues than low-value neighborhoods.

Second, we could incorporate additional socioeconomic covariates, such as median household income, population density, or demographic composition, from other public datasets. This would allow us to build regression or multilevel models that control for confounders and test whether the observed correlation between housing prices and risk proportions persists after adjustment. However, any such analysis would require careful ethical consideration to avoid stigmatizing specific communities.

Third, we could move beyond ZIP codes to more granular spatial units, such as census tracts or even exact coordinates (if available and ethically appropriate). Finer-grained spatial analysis might detect local clusters of high-risk establishments within otherwise high-value ZIP codes, or identify “food safety hot spots” that are invisible at the aggregate level. Combining GIS tools with our current pipeline would also enable map-based visualizations that are more intuitive for policymakers.

Finally, from a data-management perspective, future work could extend our Snakemake workflow to include automated tests, parameterized analysis (e.g., different time windows for ZHVI averages), and dashboard-style outputs. These enhancements would not only improve reproducibility but also make it easier for other researchers or city officials to reuse and adapt the pipeline for their own questions.

# 6\. Reproducing this project

To reproduce our results from scratch on a new machine, a reader should follow the steps documented in our workflow automation documentation and reproducibility package (please see workflow automation documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/06\_Workflow\_Automation.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/06_Workflow_Automation.md), reproducibility documentation [https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/07\_Reproducibility\_Package.md](https://github.com/annieguzh/IS-477-Course-Project/blob/main/documentations/07_Reproducibility_Package.md) and Snakefile [https://github.com/annieguzh/IS-477-Course-Project/blob/main/Snakefile](https://github.com/annieguzh/IS-477-Course-Project/blob/main/Snakefile) referenced here):

1. **Clone the repository.** Clone the GitHub repository that contains the `scripts/`, `results/`, `docs/`, `Snakefile`, and notebooks.

2. **Set up the environment.** Create a Python virtual environment and install dependencies using `pip install -r pip_freeze.txt.` We also provide a `requirements.txt` for required dependencies.

3. **Run the full workflow (optional but recommended).** If full data acquisition is desired, run the Snakemake workflow from the project root. This will execute the acquisition, storage, cleaning, integration, and analysis scripts in order, producing the raw, processed, and results files described in this report.

4. **Reproduce from archived data (offline option).** If network access is limited, download the archived processed datasets and results from the Box folder and place them in `data/processed/` and `results/` as documented (please see Box folder link referenced here [https://uofi.box.com/s/94apkk14xbqhhi5r0gk06bscn58w155c](https://uofi.box.com/s/94apkk14xbqhhi5r0gk06bscn58w155c)). The Snakemake workflow can then be configured to start from the cleaning or integration stages.

5. **Inspect the workflow notebook.** Finally, open the `workflow.ipynb` notebook to inspect intermediate outputs and replicate the exploratory steps that guided our design (please see workflow notebook referenced here [https://github.com/annieguzh/IS-477-Course-Project/blob/main/workflow.ipynb](https://github.com/annieguzh/IS-477-Course-Project/blob/main/workflow.ipynb)). 

Together, these artifacts \- scripts, Snakemake rules, checksum files, Box snapshots, and written documentation \- are intended to make the project transparent and reproducible for both graders and future collaborators.

# 7\. References

City of Chicago. *Food Inspections* dataset. Chicago Data Portal. Accessed via the official API.

* [https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about\_data](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about_data)

Zillow Research. *Zillow Home Value Index (ZHVI)* data. Zillow Research Data, for academic/non-commercial use with attribution. 

* [https://www.zillow.com/research/data/](https://www.zillow.com/research/data/)

