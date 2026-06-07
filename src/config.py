from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import urllib

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.env'))

server = os.getenv("DB_SERVER")
database = os.getenv("DB_TARGET")
driver = os.getenv("DB_DRIVER")

params = urllib.parse.quote_plus(
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", pool_pre_ping=True)