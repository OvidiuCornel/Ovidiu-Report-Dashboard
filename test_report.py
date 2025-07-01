import pytest
from report.dashboard import report_component
from python-package.employee_events.employee import Employee

def test_report_render_generates_valid_html():
    # Arrange
    dummy_entity_id = 1
    model = Employee(employee_id=dummy_entity_id)

    # Act
    html_output = report_component.render(dummy_entity_id, model)

    # Assert
    assert isinstance(html_output, str), "Outputul trebuie să fie un string"
    assert "<div" in html_output or "<h1" in html_output, "Outputul trebuie să conțină taguri HTML"
    assert "Error" not in html_output, "Nu trebuie să apară mesaje de eroare în HTML"
