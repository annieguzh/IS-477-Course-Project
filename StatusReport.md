## Tasks accomplished

So far we mainly focused on building the data pipeline in the notebook workflow.ipynb. 

#### Data Collection & Acquisition

We downloaded the Chicago Food Inspections dataset from the Socrata API, saved it as data/raw/food\_inspections.csv, and wrote a matching SHA 256 checksum file in data/raw/food\_inspections.sha256. We downloaded the ZHVI home value data using its csv url and saved into data/raw/zhvi.csv and created data/raw/zhvi.sha256 for integrity checking.

#### Data Storage & Organization

We set up a simple folder structure with data/raw for original downloads and data/processed for cleaned and integrated outputs. All important csv files in the processed folder also have SHA 256 checksum text files, so later we can verify that files have not changed.

#### Data Quality & Cleaning

For the food inspections data, we selected the main variables for our project, such as zip code, risk level, facility type, inspection date, inspection result and location, and created a reduced table with only these columns. We then cleaned this table by dropping rows with missing values, converting inspection\_date to a proper date type, creating an establishment\_id that combines license number and address, and keeping only the most recent inspection for each establishment. We also standardised the zip column into five digit strings and removed clearly invalid zip codes. The cleaned table was saved as data/processed/food\_inspections\_cleaned.csv, together with data/processed/food\_inspections\_cleaned.sha256.

For the ZHVI data, we profiled the table, identified all monthly date columns, and renamed RegionName to zip so that it matches the food data. We then created three housing indicators at the zip level, which are avg\_zhvi\_all\_time, avg\_zhvi\_recent using dates from 2020 onward, and zhvi\_latest using the most recent month. We removed zip codes that had no data in the most recent twelve months and saved the cleaned table as data/processed/zhvi\_cleaned.csv with its checksum in data/processed/zhvi\_cleaned.sha256.

#### Data Integration

We integrated the cleaned food and housing tables using “zip” as the common key. We merged the food\_inspections\_cleaned table with the housing subset that contains zip, geographic information and the three ZHVI indicators, using an inner join. The result is the integrated\_food\_housing table stored in data/processed/integrated\_food\_housing.csv, with a checksum file data/processed/integrated\_food\_housing.sha256. The workflow notebook also prints basic summaries for this integrated table, such as record counts, number of zip codes, risk distribution and simple statistics for zhvi\_latest, so that we can quickly check that the integration worked as expected.

## 

## Tasks remaining and updated focus

We have completed tasks up until data integration. Our remaining work is mainly on the analysis and documentation side. 

#### Data Analysis & Visualization

Using the integrated\_data table as our main dataset, we still need to carry out more systematic exploratory data analysis and visualization to directly connect the proportions of different risk categories to housing values across zip codes in Chicago. 

#### Workflow Automation & Provenance 

We also plan to organize the existing code into a clearer and possibly more automated workflow, with explicit notes on how each raw file turns into each processed and integrated file, so that the data provenance is easy to follow.

#### Reproducibility & Transparency 

In addition, we have not yet created separate materials for reproducibility and transparency, such as a short guide that explains how to rerun the notebook from scratch or a structured document that describes each variable in the cleaned and integrated tables. 

These remaining parts will be the main focus for the next milestones.

## 

## Updated timeline and task status

In the original project plan, our work was divided into several phases that go from defining the research question to preparing the final report and presentation. Up to this interim milestone, we have finished the phases that focus on data preparation and integration, and we are about to move into the analysis phase. The work in workflow.ipynb covers the collection of the Chicago Food Inspections data and the ZHVI housing data, the organization of raw and processed folders, the cleaning of both tables, the construction of housing features at the zip code level, and the integration step that links food inspections with housing values. These steps correspond to the early data related phases in the plan and are now complete.

Looking ahead, the remaining phases in the plan focus on exploratory data analysis, formal analysis, interpretation, and final documentation. With the integrated\_food\_housing table already produced in the processed folder, we are ready to start the next stage where we summarise and visualise the relationship between risk levels and housing values across zip codes. The upcoming weeks will therefore be used to build plots, run basic statistical checks on the integrated data, and then write up the results and conclusions. Overall, the structure of the original timeline still fits our progress, and the main change is that the data phases are now captured more clearly inside the single workflow notebook and in the set of processed csv files and checksum files.

Below is an updated timeline for the rest of the semester:   
**Statistical Analysis and Modeling (Nov 12 – Nov 24\)**  
We will conduct a correlation analysis to examine the relationship between the proportion of low-risk versus high-risk restaurants and housing prices across ZIP codes.  
**Final Results and Interpretation (Nov 25 – Dec 3\)**  
We will interpret the analysis results, draw meaningful conclusions, and prepare figures and tables for the final report.  
**Final Report (Dec 4 – Dec 10\)**  
We will finalize the GitHub repository, complete the project documentation and README, and submit the final project report.

## 

## Changes relative to the original project plan

In terms of overall direction, we did not change the main goal or the main research questions from the original project plan. We still focus on the City of Chicago Food Inspections data and the ZHVI housing data, we still use zip code as the common geographic unit, and we still want to understand how the distribution of low risk and high risk establishments relates to housing values. The scope and the datasets therefore remain the same as what we described before.

The main changes happened at the implementation level. In the plan, the data work was described as data collection, cleaning, storage, and integration as separate items. In the current milestone, we made this structure more concrete in workflow.ipynb by organizing the work into 5 clear tasks, which are data collection and acquisition, storage and organization, extraction and enrichment, data quality and cleaning, and data integration. Each of these tasks now has specific code, input files in the raw folder, and output files in the processed folder, together with sha256 checksum files. This makes the original plan more detailed but keeps the same logic.

So far we did not need to change the research question, the choice of variables, or the planned analysis steps based on earlier milestones. Instead, the current work mainly strengthens the technical side of the plan by adding a consistent directory structure, by adding checksum files for every important csv, and by producing a single integrated table that will be reused in later analysis. If we receive more detailed feedback in the next milestone, we will adjust the later analysis or visualisation plan on top of this existing workflow rather than changing the core question.

## 

## Team member contributions 

For this milestone we mainly worked together around the workflow.ipynb notebook and the data preparation pipeline. We both participated in planning how to split the work into the 5 tasks written in the section above and in checking that the files in the raw and processed folders are correctly named and saved. We discussed the choice of key variables, such as the use of zip code as the join key and the selection of risk and housing indicators, so that the later analysis will be easier to carry out.

From the coding side, Annie focused more on writing and running the Python code in the notebook. This includes calling the Chicago open data API and the Zillow csv download, saving the raw csv files, computing and writing the sha256 checksums, cleaning the food inspection table, constructing the housing features, and merging the cleaned tables into the integrated dataset. From the checking side, Judy focused more on reading through the outputs, comparing them with the original project plan, and making sure that the structure of the workflow matches what we promised in the plan. This includes reviewing the printed summaries for each step, making sure that the cleaned tables contain the expected columns, and confirming that the integration really uses zip code as the shared key.

Overall, both members contributed to this milestone by making sure that the raw data are downloaded and stored correctly, that the cleaning steps are documented and reproducible, and that the integrated\_food\_housing dataset is ready for the analysis phases in the next milestone.

