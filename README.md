
==================================================================
# Geopolitical Risk Engine
==================================================================

Welcome to the **Geopolitical Risk Engine** repository!

This project analyzes simulated historical data on global conflicts through a full ETL pipeline extended with machine learning prediction step.

A PoissonRegressor model forecasts conflict frequency per country for 2025-2026 and appends predictions to the historical dataset. Fact tables *fact_conflicts* and *fact_country_conflict_predictions* are loaded into SQL Server and connected to a Power BI dashboard via DirectQuery.


## Business Context
Organizations involved in geopolitical risk assessment, policy research, journalism, and international affairs often need to understand historical conflict patterns and identify regions with elevated levels of activity.

This project demonstrates how an ETL pipeline can transform raw conflict records into an analytics-ready dataset that supports both descriptive and predictive analysis.

The solution enables users to:
- Analyze conflict trends over time across frequency, economic loss, and casualties.
- Explore geographical distribution of conflicts by GDP gap, resource dispute, conflict type and outcome.
- Compare historical patterns with 2025-2026 forecasts derived from Poisson regression model.


## Architecture
```
    Historical Conflict Dataset
                ↓
        Python ETL + Predict
                ↓
            SQL Server
                ↓
        Power BI Dashboard
```


## Prerequisites
To reproduce the full workflow locally, Python, SQL Server Management Studio, and Power BI Desktop are recommended.


## Setup & Usage
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate virtual environment: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure paths: create config.env file inside config folder and add server name, dataset name and SQL Server driver as shown in the config.env.example
6. Run the pipeline: `python main.py`
7. Check fact tables inside SQL Server database (name can be checked in config.env file)
8. Open .pbit file inside powerbi folder
9. Power BI asks for connection information: use SQL Server name and database name and connect data using DirectQuery option
10. Tables can be further updated in SQL Server, but Power BI refreshes the data and visuals populate automatically. Well done!


## Tech Stack
- Python (Pandas, NumPy, Scikit-learn)
- SQL Server
- Power BI


## Project structure
```
│   .gitignore                                  # Files and directories to be ignored by Git
│   LICENSE                                     # License information for the repository
│   main.py                                     # The main entry point of the project. Runs ETL pipeline: extract -> transform -> predict -> load
│   README.md                                   # Project overview and instructions
│   requirements.txt                            # Dependencies and requirements for the project
│   
├───config                                      ## Config files
│       config.env.example                      # Example of .env file with keys
│       
├───data                                        ## Datasets
│       global_conflicts_anomalies.csv          # Dataset for the period 1950-2024
│           
├───powerbi                                     ## Power BI outputs
│       geopolitical-risk-engine.pbit           # Power BI template
│       geopolitical-risk-engine.pdf            # PDF file with screenshots of all the Power BI dashboard pages
│       
├───sql                                         ## SQL queries
│       vw_economic_loss_by_conflict_type.sql   # Conflict_Type + Total_Economic_Loss + Average_Economic_Loss
│       vw_gdp_gap_group_stats.sql              # GDP_Gap_Label + Conflict_Count + Avg_Economic_Loss + Total_Economic_Loss + Avg_Deaths + Total_Deaths
│       vw_war_involvment.sql                   # Country + War_Involvment_Count
│       vw_yearly_trend.sql                     # Year + Total_Conflicts + Total_Deaths + Total_Economic_Loss
│       
└───src                                         ## ETL stage of project
        columns.py                              # List of columns used in transform function
        _01_extract.py                          # Extracts data from .csv dataset
        _02_transform.py                        # Selects columns, filters dataset, adds calculations
        _03_predict.py                          # PoissonRegressor model predicts conflict frequency per country (2025-2026): Country + Year + Conflict_Count
        _04_load.py                             # Fact tables fact_conflicts and fact_country_conflict_predictions load into SQL Server
```


### sql
SQL Server was used during exploratory stage of data aggregation and evolution. The final production workflow relies primarily on Python ETL and Power BI.
Some of SQL views findings were used later in Power BI dashboard.


### src
Full ETL pipeline with additional forecast step. Extracts raw conflict data, transforms and filters it, aggregates historical conflict frequency per country, predicts 2025-2026 values using PoissonRegressor, and loads two fact tables into SQL Server.


### powerbi
Four-page Power BI dashboard supports exploratory analysis of global conflict data.

- **Executive Overview** - KPIs, conflict frequency by year, globe visualization
- **Conflicts Impact Analysis** - military and civilian deaths, economic loss by conflict type, country and year
- **Geopolitical Analysis** - conflict map filtered by outcome, resource dispute, GDP gap and conflict type
- **Trends & Forecasting** - PoissonRegressor predictions for 2025-2026, historical matrix heatmap


## Future improvements
- Incorporate real-world conflict datasets.
- Evaluate additional forecasting models.
- Automate ETL scheduling.
- Publish dashboard through Power BI Service.
