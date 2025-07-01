# db_utils.py
from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "employee_events.db"

def run_query(query, params=None, db_path=DB_PATH):
    if not db_path.exists():
        raise FileNotFoundError(f"Baza de date nu există la: {db_path}")
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
