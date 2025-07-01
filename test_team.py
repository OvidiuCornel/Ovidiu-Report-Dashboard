import sqlite3

def check_team_exists(team_id, db_path="python-package/employee_events/employee_events.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT team_name FROM team WHERE team_id = ?", (team_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"Team {team_id} exists: {row[0]}")
        return True
    else:
        print(f"Team {team_id} does NOT exist.")
        return False

# Testează dacă echipa cu ID 3 există
check_team_exists(3)
