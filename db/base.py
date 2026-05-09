from sqlalchemy import create_engine
from urllib.parse import quote_plus
from core.config import Config

connection_string = (
    f"DRIVER={Config.DB_DRIVER};"
    f"SERVER={Config.DB_SERVER};DATABASE={Config.DB_NAME};UID={Config.DB_USER};PWD={Config.DB_PASSWORD};"
)
print(connection_string)


# 🔐 encode برای SQLAlchemy
params = quote_plus(connection_string)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=True  # موقت برای debug
)