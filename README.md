
<h1 align=>Geopolitical Risk Engine</h1>

<p align=>
ETL Pipeline • Machine Learning Forecasting • SQL Server • Power BI
</p>

Welcome to the **Geopolitical Risk Engine** repository!

This project transforms simulated historical conflicts data through a full ETL pipeline with SQL data warehouse layers, machine learning forecasting and Power BI reporting.

A PoissonRegressor ML model predicts conflict frequency per country for 2025-2026 and appends results to the historical data. Data is staged through raw, staging and analytics schemas in SQL Server. Power BI connects to *fact_conflicts* and *fact_country_conflict_predictions* via DirectQuery, which are views mapped to the analytics schema tables.


## Business Context

Organizations involved in geopolitical risk assessment, policy research, journalism, and international affairs often need to understand historical conflict patterns and identify regions with elevated levels of activity.

This project demonstrates how an ETL pipeline can transform raw conflict records into an analytics-ready dataset that supports both descriptive and predictive analysis.

The solution enables users to:
- Analyze conflict trends over time across frequency, economic loss, and casualties.
- Explore geographical distribution of conflicts by GDP gap, resource dispute, conflict type and outcome.
- Compare historical patterns with 2025-2026 forecasts derived from Poisson regression model.


## Architecture
[Visual Architecture Diagram](docs/architecture.png)

<div align="center">

Historical Conflict Dataset

↓

Python ETL  / / Extract → Validate → Transform → Predict (ML) → Load  / /

↓

SQL Server  / / Raw → Staging → Analytics  / /

↓

Power BI Dashboard

</div>


## Power BI Dashboard
[Power BI Dashboard PDF](powerbi/geopolitical-risk-engine.pdf)


## Prerequisites
To reproduce the full workflow locally, VSCode, Python, SQL Server Management Studio, and Power BI Desktop are recommended.


## Setup & Usage
1. Clone the repository.
2. Create virtual environment: `python -m venv .venv`.
3. Activate virtual environment: `.venv\Scripts\activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run create_database.sql from sql folder to create SQL Server database.
6. Create config.env file inside config folder, copy everything from config.env.example and replace DESKTOP-NAME with your actual desktop name or replace full SQL Server name with the one you have. 
7. Run create_schemas.sql from sql folder to create SQL Server schemas.
8. Run the pipeline: `python main.py` in terminal from the project folder.
9. Check fact tables inside SQL Server database geopolitical_risk_engine.
10. Open .pbit file inside powerbi .
11. If Power BI asks for connection information: use SQL Server name and database name and connect data using DirectQuery option.
12. Tables can be further updated in SQL Server. Power BI visuals should populate automatically after refresh.


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
├───docs                                        ## Architecture
│       architecture.pdf                        # Visual architecture of the pipeline
│ 
├───powerbi                                     ## Power BI outputs
│       geopolitical-risk-engine.pbit           # Power BI template
│       geopolitical-risk-engine.pdf            # PDF file with screenshots of all the Power BI dashboard pages
│       
├───sql                                         ## SQL queries
│       create_database.sql                     # Creates SQL Server database
│       create_schemas.sql                      # Creates SQL Server schemas for ETL tables upload for each data processing stage
│       create_views.sql                        # Creates SQL Server views required for PowerBI compatibility
│       
└───src                                         ## ETL stage of project                         
    │   columns.py                              # List of columns selected for further analysis
    │   config.py                               # SQL Server connector
    │   pipeline_logger.py                      # Settings of ETL Pipeline output
    │   _01_extract.py                          # Extracts data from .csv dataset and from SQL Server
    │   _02_validate.py                         # Dataset normalization with phases: deduplicate, standardize, handle_nulls
    │   _03_transform.py                        # Selects columns, filters dataset, adds calculations
    │   _04_predict.py                          # PoissonRegressor model predicts conflict frequency per country (2025-2026): Country + Year + Conflict_Count
    └───_05_load.py                             # Load of raw, staging and analytics tables into SQL Server
```

## Key folders

### sql
Database, schemas and views creation queries essential for project formation.


### src
Full ETL pipeline with additional forecast step. Extracts raw conflict data, validates, transforms and filters it, aggregates historical conflict frequency per country, predicts 2025-2026 values using PoissonRegressor, and loads each stage result, including two fact tables into SQL Server.


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
