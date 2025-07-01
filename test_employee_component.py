from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()

# Modelul fictiv
class FakeEmployeeModel:
    def get_user_type_names_and_ids(self):
        return [
            (1, "Ana Popescu"),
            (2, "Ion Ionescu"),
            (3, "Maria Georgescu")
        ]

# Componenta de tip tabel HTML
class DataTable:
    def __init__(self, model):
        self.model = model

    def render(self):
        data = self.get_data()
        table_html = "<table border='1'>"
        table_html += "<tr><th>ID</th><th>Name</th></tr>"

        for row in data:
            table_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"

        table_html += "</table>"
        return table_html

    def get_data(self):
        return self.model.get_user_type_names_and_ids()

# Ruta principală
@app.get("/", response_class=HTMLResponse)
def read_table():
    model = FakeEmployeeModel()
    table = DataTable(model)
    html_content = f"""
    <html>
        <head><title>Employee Table</title></head>
        <body>
            <h1>Lista Angajați</h1>
            {table.render()}
        </body>
    </html>
    """
    return html_content
