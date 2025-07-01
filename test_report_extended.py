import pytest
import pandas as pd
from report.dashboard import Report, ReportDropdown, Visualizations, NotesTable, DashboardFilters, Header
from python-package.employee_events.employee import Employee
from python-package.employee_events.team import Team

# --- Teste pentru Report.render() ---

def test_report_render_employee_clean_html():
    employee = Employee(employee_id=1)
    report = Report()
    html = report.render(1, employee)
    # Verificăm că tag-ul <h1> apare ne-escapat
    assert isinstance(html, str)
    assert "<h1>Report Dashboard</h1>" in html
    assert "&lt;h1&gt;" not in html

def test_report_render_team_clean_html():
    team = Team(team_id=1)
    report = Report()
    html = report.render(1, team)
    assert isinstance(html, str)
    assert "<h1>Report Dashboard</h1>" in html

def test_report_render_with_invalid_model():
    class DummyModel:
        pass
    dummy = DummyModel()
    report = Report()
    html = report.render(1, dummy)
    # Nu trebuie să crash-uiască, ci să întoarcă un string de eroare
    assert isinstance(html, str)
    assert "Error" in html or "<div" in html

def test_report_render_with_none_entity():
    employee = Employee(employee_id=1)
    report = Report()
    html = report.render(None, employee)
    assert isinstance(html, str)

# --- Teste pentru ReportDropdown ---

def test_reportdropdown_component_data_returns_list():
    dropdown = ReportDropdown(id="selector", name="user-selection")
    employee = Employee(employee_id=1)
    data = dropdown.component_data(None, employee)
    assert isinstance(data, (list, tuple))
    # Fiecare element trebuie să fie un tuple/id+name
    assert all(isinstance(item, (list, tuple)) and len(item) == 2 for item in data)

# --- Teste pentru Visualizations ---

def test_visualizations_with_mock_model_data():
    class ModelWithData:
        def model_data(self):
            return pd.DataFrame({
                'event_date': ['2025-01-01', '2025-01-02'],
                'positive_events': [5, 10],
                'negative_events': [3, 4]
            })

    vis = Visualizations()
    model = ModelWithData()
    div = vis(None, model)
    # Așteptăm un Div cu 2 copii
    assert div is not None
    assert hasattr(div, 'children')
    assert len(div.children) == 2

# --- Teste pentru NotesTable ---

def test_notes_table_component_data_dataframe():
    class ModelWithNames:
        def get_names(self, entity_id=None):
            return [
                ['1', 'Alice'],
                ['2', 'Bob'],
            ]

    notes = NotesTable()
    df = notes.component_data(None, ModelWithNames())
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['ID', 'Name']
    assert df.shape[0] == 2

# --- Teste pentru DashboardFilters ---

def test_dashboardfilters_structure():
    filters = DashboardFilters()
    assert isinstance(filters.children, list)
    assert len(filters.children) == 2
    # Prima este Radio, a doua ReportDropdown
    from report.base_components.radio import Radio
    from report.dashboard import ReportDropdown
    assert isinstance(filters.children[0], Radio)
    assert isinstance(filters.children[1], ReportDropdown)

# --- Test pentru Header ---

def test_header_build_component():
    header = Header()
    html = header.build_component()
    assert html == "<h1>Report Dashboard</h1>"
