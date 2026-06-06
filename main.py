from dotenv import load_dotenv
import os
from src._01_extract import extract
from src._02_transform import transform
from src.columns import columns
from src._03_predict import conflict_involvment_prediction
from src._04_load import load

load_dotenv(os.path.join(os.path.dirname(__file__), 'config', 'config.env'))

server = os.getenv("DB_SERVER")
database = os.getenv("DB_TARGET")
driver = os.getenv("DB_DRIVER")

if __name__ =="__main__":

    print("=" * 60)
    print('=== Geopolitical Risk Egnine ETL Pipeline ==='.center(60))
    print("=" * 60)

    df = extract("data/global_conflicts_anomalies.csv")
    df = transform(df, columns)
    table = conflict_involvment_prediction(df)
    load(df, table, server, database, driver)

    print("=" * 60)
    print('=== ETL complete ✅ ==='.center(60))
    print("=" * 60)
