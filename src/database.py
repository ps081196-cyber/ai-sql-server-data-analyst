"""SQL Server connection and schema helpers."""
import os
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, inspect, text

def build_engine():
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    odbc = quote_plus(
        f"DRIVER={{{driver}}};SERVER={os.environ['SQL_SERVER']};"
        f"DATABASE={os.environ['SQL_DATABASE']};UID={os.environ['SQL_USERNAME']};"
        f"PWD={os.environ['SQL_PASSWORD']};Encrypt=yes;TrustServerCertificate=yes"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={odbc}", pool_pre_ping=True)

def schema_summary(engine, max_tables: int = 30) -> str:
    inspector = inspect(engine)
    lines = []
    for table in inspector.get_table_names()[:max_tables]:
        cols = inspector.get_columns(table)
        lines.append(f"{table}({', '.join(c['name'] for c in cols)})")
    return "\n".join(lines)

def run_query(engine, sql: str) -> pd.DataFrame:
    with engine.connect() as connection:
        return pd.read_sql(text(sql), connection)
