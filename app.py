from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
from fasthtml.core import Table, Tr, Th, Td

class DataTable:
    def build_component(self, entity_id, model):
        data = self.component_data(entity_id, model)
        header = Tr(*(Th(col) for col in data.columns))
        rows = [Tr(*(Td(cell) for cell in row)) for row in data.itertuples(index=False)]
        return Table(header, *rows)

    def component_data(self, entity_id, model):
        # Date demo
        return pd.DataFrame([
            (1, "Ana Popescu"),
            (2, "Ion Ionescu"),
            (3, "Maria Georgescu"),
        ], columns=["ID", "Name"])

    def __call__(self, entity_id, model):
        component = self.build_component(entity_id, model)
        return component

app = FastAPI()
table = DataTable()

@app.get("/", response_class=HTMLResponse)
async def home():
    component_html = table(None, None)
    return HTMLResponse(content=str(component_html))
