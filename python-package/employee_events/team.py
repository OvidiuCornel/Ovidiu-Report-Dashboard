import pandas as pd
from .query_base import QueryBase
from .db_utils import DB_PATH


class Team(QueryBase):
    def __init__(self, team_id, db_path=DB_PATH):
        super().__init__(db_path)
        self.team_id = int(team_id)
        self._name = None
        self._load_name()

    def _load_name(self):
        query = "SELECT team_name FROM team WHERE team_id = ?"
        df = pd.read_sql_query(query, self.connection, params=(self.team_id,))
        self._name = df.iloc[0, 0] if not df.empty else "Unknown"

    @property
    def name(self):
        return self._name

    def model_data(self, _=None):
        query = """
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee_events
            WHERE team_id = ?
            GROUP BY event_date
            ORDER BY event_date
        """
        return pd.read_sql_query(query, self.connection, params=(self.team_id,))

    def get_names(self, _=None):
        query = """
            SELECT team_id, team_name
            FROM team
            ORDER BY team_name
        """
        df = pd.read_sql_query(query, self.connection)
        return df.values.tolist()

    def get_user_type_names_and_ids(self):
        query = "SELECT team_id, team_name FROM team ORDER BY team_name"
        df = pd.read_sql_query(query, self.connection)
        return list(zip(df['team_name'], df['team_id']))  # (label, value)

    def notes(self, team_id=None):
        if team_id is None:
            team_id = self.team_id
        query = """
            SELECT note_date, note
            FROM notes
            WHERE team_id = ?
            ORDER BY note_date DESC
        """
        return pd.read_sql_query(query, self.connection, params=(team_id,))
        
