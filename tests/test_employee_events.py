import pytest
from pathlib import Path
import sqlite3

# Using pathlib create a project_root
# variable set to the absolute path
# for the root of this project
project_root = Path(__file__).resolve().parents[2]

# apply the pytest fixture decorator
# to a `db_path` function
@pytest.fixture
def db_path(tmp_path):
    # Example: create a path for a temporary test database file
    path = tmp_path / "test_db.sqlite"
    path.touch()  # This creates an empty file at the path
    return path

    # Using the `project_root` variable
    # return a pathlib object for the `employee_events.db` file
def get_employee_db_path(project_root: Path) -> Path:
    return project_root / "employee_events.db"

# Define a function called
# `test_db_exists`
# This function should receive an argument
# with the same name as the function
# the creates the "fixture" for
# the database's filepath
def test_db_exists(db_path):
    # Check if the database file exists (or not, depending on test context)
    assert not db_path.exists(), "Database file should not exist yet"

    # using the pathlib `.is_file` method
    # assert that the sqlite database file exists
    # at the location passed to the test_db_exists function
def test_db_exists(db_path):
    assert db_path.is_file(), "Expected database file to exist at the given path"

@pytest.fixture
def db_conn(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Create tables
    cursor.execute("CREATE TABLE employee (id INTEGER PRIMARY KEY, name TEXT);")
    cursor.execute("CREATE TABLE team (id INTEGER PRIMARY KEY, name TEXT);")
    cursor.execute("CREATE TABLE employee_events (id INTEGER PRIMARY KEY, event_name TEXT);")
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# Define a test function called
# `test_employee_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_employee_table_exists(table_names):
    assert "employee" in table_names, "Expected 'employee' table to exist in the database"

    # Assert that the string 'employee'
    # is in the table_names list
def test_employee_table_exists(table_names):
    assert 'employee' in table_names, "'employee' table not found in the database"

# Define a test function called
# `test_team_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_team_table_exists(table_names):
    assert 'team' in table_names, "'team' table not found in the database"


    # Assert that the string 'team'
    # is in the table_names list
    assert 'team' in table_names

# Define a test function called
# `test_employee_events_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_employee_events_table_exists(table_names):
    assert 'employee_events' in table_names, "'employee_events' table not found in the database"


    # Assert that the string 'employee_events'
    # is in the table_names list
    assert 'employee_events' in table_names, "'employee_events' table not found in the database"
