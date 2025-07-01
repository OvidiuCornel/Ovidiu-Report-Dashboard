from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path("employee_events.db").resolve()


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query, params=None):
        """
        Executes the given SQL query and returns the result as a pandas DataFrame.
        Assumes the class using this mixin has a self.connection attribute (sqlite3 connection).
        """
        if params:
            return pd.read_sql_query(sql_query, self.connection, params=params)
        else:
            return pd.read_sql_query(sql_query, self.connection)

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query, params=None):
        """
        Executes the given SQL query and returns the result as a list of tuples.
        Assumes the class using this mixin has a self.cursor attribute (sqlite3 cursor).
        """
        if params:
            self.cursor.execute(sql_query, params)
        else:
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()



 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result

    return run_query
