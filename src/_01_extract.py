from src.pipeline_logger import log
import pandas as pd
from src.config import engine

def extract_from_csv(filepath):
    df = pd.read_csv(filepath)
    log.kv("source rows", len(df))
    log.kv("source columns", len(df.columns))
    return df

def extract_from_sql(table, schema):
    df = pd.read_sql(f"SELECT * FROM [{schema}].[{table}]", engine)
    log.kv("source rows", len(df))
    return df