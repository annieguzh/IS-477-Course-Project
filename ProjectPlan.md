**Overview**  
The goal of our project is to explore how food safety risk levels, specifically the proportion of “low-risk” and “high-risk” restaurants, may influence housing prices in neighborhoods of Chicago. By integrating Chicago’s Food Inspections data with Zillow’s Housing Prices dataset, we aim understand whether areas with better food safety records tend to have higher property values.   
The motivation behind our project stems from the idea that local health conditions and regulatory enforcement, reflected through restaurant inspection outcomes, can indirectly impact how desirable a neighborhood is, which in turn may be captured through housing market dynamics. By analyzing these relationships, we can gain insights into how public health indicators may act as socioeconomic signals in urban environments. 

**Research Questions**

* Does the proportion of “low-risk” versus “high-risk” food establishments in a ZIP code area correlate with local housing prices?  
* Are there particular regions (ZIP codes or community areas) in Chicago where this relationship is stronger or weaker?

**Team**  
Our project team consists of two members:  
Judy – Responsible for data collection, cleaning, and integration. Judy will prepare the food inspection and housing price datasets, merge them by ZIP code, and ensure the data is properly structured for analysis.  
Annie – Responsible for exploratory data analysis, visualization, and statistical analysis. Annie will examine the relationship between food safety risk proportions and housing prices and interpret the results.  
Both members will collaborate on writing the Interim Status Report and Final Project Report.

**Datasets**  
We will use two datasets from different sources and integrate them by ZIP code to analyze the relationship between food safety risk levels and local housing prices.

1. City of Chicago Food Inspections Dataset  
   Source: [https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about\_data](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/about_data)  
     
   Description:   
   This dataset contains detailed records of food safety inspections conducted by the City of Chicago Department of Public Health. Each record includes inspection date, facility type, risk category (low, medium, or high), results (pass/fail), and geographic information (address, latitude/longitude, community area, and ZIP code).   
     
   Use in our project:   
   We will focus on the “Risk” column to calculate the proportion of “low-risk” and “high-risk” establishments in each ZIP code. This will be used as our key.   
     
   Ethical & legal consideration:   
* Public data released under the City of Chicago’s Open Data License  
* No personally identifiable information  
* Must cite the City of Chicago as the data source  
    
    
2. Zillow Home Value Index (ZHVI) Dataset  
   Source:   
   [https://www.zillow.com/research/data/](https://www.zillow.com/research/data/)  
     
   Description:   
   This dataset contains Zillow Home Value Index (ZHVI) estimates at various geographic resolutions (zip code, city, metro, county) for Chicago. Each observation represents median housing price estimates over time.  
     
   Use in our project:   
   We will calculate the average housing prices over a period of time (decided later in the project), and integrate it with the Food Inspection Dataset.  
     
   Ethical & legal consideration:   
* Zillow Research data is provided for academic/non-commercial use with attribution  
* Terms of use must be followed, and derivative data products must reference Zillow

Integration Plan:

* Both datasets contain ZIP codes, which will serve as the primary key for merging   
* We will preprocess the data to remove missing or invalid ZIP codes and ensure consistent formatting  
* We will aggregate the food inspection data by ZIP code to calculate the proportion of low-risk vs. high-risk establishments  
* We will align the time periods of both datasets (e.g., by selecting overlapping years or aggregating by year) before conducting correlation analysis

**Timeline**  
Our project will follow a structured timeline divided into eight main phases throughout the semester.  
**Phase 1: Project Planning (Sep 26 – Oct 7\)**  
During this phase, we will finalize our research question, select the datasets we plan to use, and complete the initial version of the ProjectPlan.md.  
**Phase 2: Data Acquisition, Collection, and Cleaning (Oct 8 – Oct 21\)**  
Judy will access both datasets using API/CSV, examine their structure and verify metadata, clean missing or inconsistent records, and standardize the ZIP code format to prepare them for integration.  
**Phase 3: Data Storage & Integration (Oct 22 – Oct 28\)**  
Judy will select a storage strategy. Then merge the food inspection and housing price datasets by ZIP code, calculate the proportions of low-risk and high-risk food establishments, and align the time periods between the two datasets.  
**Phase 4: Exploratory Data Analysis (Oct 29 – Nov 10\)**  
Annie will conduct exploratory data analysis, including descriptive statistics, visualizations, and initial correlation checks between food safety risk levels and housing prices.  
**Phase 5: Interim Status Report (Nov 11\)**  
Annie and Judy will work together to prepare and submit a two-page progress report summarizing preliminary findings and outlining the next steps.  
**Phase 6: Statistical Analysis and Modeling (Nov 12 – Nov 24\)**  
Annie will conduct a correlation analysis to examine the relationship between the proportion of low-risk versus high-risk restaurants and housing prices across ZIP codes.  
**Phase 7: Final Results and Interpretation (Nov 25 – Dec 3\)**  
Annie will interpret the analysis results, draw meaningful conclusions, and prepare figures and tables for the final report.  
**Phase 8: Final Report and Presentation (Dec 4 – Dec 10\)**  
Annie and Judy will collaborate to finalize the GitHub repository, complete the project documentation and README, and submit the final project report and presentation.

**Constraints**  
While our project is feasible within the course timeline, we anticipate several potential constraints that may affect our progress and results:

1. **Data Availability and Coverage:**  
   The food inspection dataset may not have uniform coverage across all ZIP codes or time periods, which could limit the number of neighborhoods included in our analysis. Additionally, some ZIP codes may have insufficient data points for reliable proportion calculations.  
2. **Temporal Alignment:**  
   The two datasets differ in their temporal resolution \- the food inspection data is event-based, while the Zillow housing data is monthly. We will address this by aggregating both datasets to a common yearly level, but some temporal details may be lost in the process.  
3. **Data Quality and Consistency:**  
   Missing, incomplete, or inconsistent entries (e.g., invalid ZIP codes or missing risk levels) may require extensive cleaning and could reduce the amount of usable data.  
4. **External Factors Not Captured:**  
   Housing prices are influenced by many variables beyond food safety (e.g., school quality, crime rate, proximity to downtown). Since our analysis focuses only on food safety risk levels, we may not capture the full range of factors influencing property values.

**Gaps**

1. We may need to confirm ZIP code provides the most stable linkage between datasets  
2. We may need to determine an appropriate statistical model (linear regression or clustering) once data integration is complete

