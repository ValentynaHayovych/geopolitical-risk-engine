from sqlalchemy import create_engine
import urllib

def load(df, table, server, database, driver):
    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", pool_pre_ping=True)

    df.to_sql(
        name="fact_conflicts", 
        con=engine,
        schema="dbo",
        if_exists="replace", 
        index=False
    )
    print(f"Loaded {len(df)} rows into fact_conflicts table of geopolitical_impact database")

    table.to_sql(
        name="fact_country_conflict_predictions", 
        con=engine,
        schema="dbo",
        if_exists="replace",
        index=False
    )
    print(f"Loaded {len(table)} rows into fact_country_conflict_predictions table of geopolitical_impact database")
