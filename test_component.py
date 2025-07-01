# test_component.py

from fasthtml.common import Table, Tr, Th, Td, Div

# Clasa de bază
class BaseComponent:
    def component_data(self, entity_id, model):
        raise NotImplementedError("component_data trebuie suprascris în subclasă.")

    def build_component(self, entity_id, model):
        raise NotImplementedError("build_component trebuie suprascris în subclasă.")

    def __call__(self, entity_id, model):
        return self.build_component(entity_id, model)

# Componentă derivată: tabel de date
class DataTable(BaseComponent):
    def component_data(self, entity_id, model):
        if hasattr(model, 'get_user_type_names_and_ids'):
            data = model.get_user_type_names_and_ids()
            import pandas as pd
            return pd.DataFrame(data, columns=['ID', 'Name'])
        else:
            raise NotImplementedError("Modelul nu are metoda get_user_type_names_and_ids")

    def build_component(self, entity_id, model):
        import pandas as pd
        data = self.component_data(entity_id, model)

        header = Tr(*(Th(col) for col in data.columns))
        rows = [Tr(*(Td(cell) for cell in row)) for row in data.itertuples(index=False)]
        return Table(header, *rows)

# Un model fals
class FakeModel:
    def get_user_type_names_and_ids(self):
        return [
            (1, "Ana Popescu"),
            (2, "Ion Ionescu"),
            (3, "Maria Georgescu"),
        ]

# Rulăm testul
if __name__ == "__main__":
    model = FakeModel()
    dt = DataTable()
    html_output = dt(entity_id=None, model=model)

    print(html_output)  # Vei vedea <table>...</table>
