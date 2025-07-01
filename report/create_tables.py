# report/create_tables.py
import sqlite3
from pathlib import Path

# Calea către fișierul .db
db_path = Path(__file__).resolve().parent.parent / "python-package" / "employee_events" / "employee_events.db"

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 1) Tabela employee
cursor.execute("""
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    name TEXT,
    team_id INTEGER
)
""")

# 2) (Opțional) Tabela team
cursor.execute("""
CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER UNIQUE,
    team_name TEXT
)
""")

# 3) (Opțional) Tabela employee_events
cursor.execute("""
CREATE TABLE IF NOT EXISTS employee_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    event_date TEXT,
    positive_events INTEGER,
    negative_events INTEGER,
    FOREIGN KEY(employee_id) REFERENCES employee(employee_id)
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_types (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
""")



conn.commit()
conn.close()
print("✅ Tabelele au fost create (dacă nu existau deja).")
