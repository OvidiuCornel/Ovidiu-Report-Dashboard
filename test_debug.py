import pandas as pd
from fasthtml.core import Table, Tr, Th, Td

class BaseComponent:

    def build_component(self, entity_id, model):
        raise NotImplementedError

    def outer_div(self, component):
        print("Calling outer_div")  # debug
        return component

    def component_data(self, entity_id, model):
        raise NotImplementedError

    def __call__(self, entity_id, model):
        print(f"__call__ started with entity_id={entity_id}")

        component = self.build_component(entity_id, model)
        print(f"Component built: {component}")

        # breakpoint aici
        import pdb; pdb.set_trace()

        wrapped = self.outer_div(component)
        print(f"Component after outer_div: {wrapped}")

        return wrapped


class DataTable(BaseComponent):

    def component_data(self, entity_id, model):
        # fake data pentru test
        data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['Ana Popescu', 'Ion Ionescu', 'Maria Georgescu']
        })
        print(f"component_data returns:\n{data}")
        return data

    def build_component(self, entity_id, model):
        data = self.component_data(entity_id, model)
        header = Tr(*(Th(col) for col in data.columns))
        rows = [Tr(*(Td(cell) for cell in row)) for row in data.itertuples(index=False)]
        table = Table(header, *rows)
        print(f"Built Table object: {table}")
        return table


if __name__ == "__main__":
    dt = DataTable()
    print("Calling component...")
    result = dt(entity_id=None, model=None)
    print("Result:", result)
