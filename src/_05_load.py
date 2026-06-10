from src.pipeline_logger import log
from src.config import engine

def load_raw(df):
    df.to_sql(
        name="global_conflicts",
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False
    )
    log.kv("loaded", f"{len(df)} rows → raw.global_conflicts")

def load_staging(df):
    df.to_sql(
        name = "global_conflicts",
        con=engine,
        schema = "staging",
        if_exists="replace",
        index=False
    )
    log.kv("loaded", f"{len(df)} rows → staging.global_conflicts")

def load_analytics(df):
    df.to_sql(
        name="fact_conflicts", 
        con=engine,
        schema="analytics",
        if_exists="replace", 
        index=False
    )
    log.kv("loaded", f"{len(df)} rows → analytics.fact_conflicts")

def load_prediction_fact(predictions):
    predictions.to_sql(
        name="fact_country_conflict_predictions", 
        con=engine,
        schema="analytics",
        if_exists="replace",
        index=False
    )
    log.kv("loaded", f"{len(predictions)} rows → analytics.fact_country_conflict_predictions")