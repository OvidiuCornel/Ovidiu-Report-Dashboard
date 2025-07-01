from pathlib import Path
from .query_base import QueryBase
import pandas as pd

class Employee(QueryBase):
    def __init__(self, employee_id, db_path="employee_events.db"):
        super().__init__(db_path)
        self.employee_id = int(employee_id)
        self._name = self._load_name()

    def _load_name(self):
        query = "SELECT first_name || ' ' || last_name FROM employee WHERE employee_id = ?"
        self.cursor.execute(query, (self.employee_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Unknown"

    @property
    def name(self):
        return self._name

    def model_data(self):
        query = """
        SELECT event_date, positive_events, negative_events
        FROM employee_events
        WHERE employee_id = ?
        ORDER BY event_date
        """
        return pd.read_sql_query(query, self.connection, params=(self.employee_id,))

    def get_names(self):
        query = """
        SELECT employee_id, first_name || ' ' || last_name AS full_name
        FROM employee
        ORDER BY full_name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_type_names_and_ids(self):
        query = "SELECT employee_id, first_name || ' ' || last_name AS name FROM employee ORDER BY name"
        self.cursor.execute(query)
        return [(row[1], row[0]) for row in self.cursor.fetchall()]  # (label, value)

    def notes(self):
        return super().get_notes(employee_id=self.employee_id)
