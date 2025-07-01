# import sqlite3
import pandas as pd
import sqlite3

class QueryBase:
    def __init__(self, db_path="employee_events.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_all_teams(self):
        query = "SELECT team_id, team_name FROM team"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_employees(self):
        query = "SELECT employee_id, first_name, last_name FROM employee"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_notes(self, employee_id=None, team_id=None):
        query = "SELECT * FROM notes WHERE 1=1"
        params = []
        if employee_id is not None:
            query += " AND employee_id = ?"
            params.append(employee_id)
        if team_id is not None:
            query += " AND team_id = ?"
            params.append(team_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


class Employee(QueryBase):
    def __init__(self, db_path="employee_events.db"):
        super().__init__(db_path)

    def get_employee_fullname(self, employee_id):
        query = "SELECT first_name, last_name FROM employee WHERE employee_id = ?"
        self.cursor.execute(query, (employee_id,))
        return self.cursor.fetchone()

    def get_employee_events(self, employee_id):
        query = """
            SELECT event_date, positive_events, negative_events
            FROM employee_events
            WHERE employee_id = ?
            ORDER BY event_date
        """
        self.cursor.execute(query, (employee_id,))
        return self.cursor.fetchall()

    def get_employee_team(self, employee_id):
        query = """
            SELECT t.team_name, t.manager_name
            FROM employee e
            JOIN team t ON e.team_id = t.team_id
            WHERE e.employee_id = ?
        """
        self.cursor.execute(query, (employee_id,))
        return self.cursor.fetchone()

    def names(self):
        query = "SELECT first_name || ' ' || last_name AS name FROM employee"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def event_counts(self, employee_id):
        query = """
            SELECT event_type, COUNT(*) as event_count
            FROM employee_events
            WHERE employee_id = ?
            GROUP BY event_type
        """
        return pd.read_sql_query(query, self.connection, params=(employee_id,))

    def daily_event_summary(self, employee_id):
        query = """
            SELECT event_date,
                   SUM(positive_events) AS total_positive_events,
                   SUM(negative_events) AS total_negative_events
            FROM employee
            JOIN employee_events USING(employee_id)
            WHERE employee.employee_id = ?
            GROUP BY event_date
            ORDER BY event_date
        """
        return pd.read_sql_query(query, self.connection, params=(employee_id,))

    def notes(self, employee_id):
        query = """
            SELECT note_date, note
            FROM notes
            WHERE employee_id = ?
            ORDER BY note_date DESC
        """
        return pd.read_sql_query(query, self.connection, params=(employee_id,))

    def employee_exists(self, employee_id):
        query = "SELECT 1 FROM employee WHERE employee_id = ?"
        self.cursor.execute(query, (employee_id,))
        return self.cursor.fetchone() is not None



class Team(QueryBase):
    def __init__(self, db_path="employee_events.db"):
        super().__init__(db_path)

    def get_team_name(self, team_id):
        query = "SELECT team_name FROM team WHERE team_id = ?"
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchone()

    def get_team_manager(self, team_id):
        query = "SELECT manager_name FROM team WHERE team_id = ?"
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchone()

    def get_team_members(self, team_id):
        query = """
            SELECT employee_id, first_name, last_name
            FROM employee
            WHERE team_id = ?
            ORDER BY last_name, first_name
        """
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchall()

    def get_all_teams(self):
        query = "SELECT team_id, team_name, manager_name FROM team"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def team_exists(self, team_id):
        query = "SELECT 1 FROM team WHERE team_id = ?"
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchone() is not None

    def notes(self, team_id):
        query = """
            SELECT note_date, note
            FROM notes
            WHERE team_id = ?
            ORDER BY note_date DESC
        """
        return pd.read_sql_query(query, self.connection, params=(team_id,))
