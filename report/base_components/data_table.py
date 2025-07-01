from fasthtml.common import Table, Tr, Th, Td
import pandas as pd
from .base_component import BaseComponent

class DataTable(BaseComponent):

    def build_component(self, entity_id, model):
        # Obține datele printr-o metodă definită în BaseComponent (sau direct din model)
        data = self.component_data(entity_id, model)  # presupunem că returnează DataFrame

        # Construim header-ul tabelului din numele coloanelor
        header = Tr(*(Th(col) for col in data.columns))

        # Construim rândurile cu date
        rows = []
        for row in data.itertuples(index=False):
            rows.append(Tr(*(Td(cell) for cell in row)))

        # Creăm obiectul tabel cu header și toate rândurile
        table = Table(header, *rows)

        return table


    def component_data(self, entity_id, model):
        # Exemplu de metodă care să întoarcă DataFrame
        # Trebuie suprascrisă sau folosește model.get_user_type_names_and_ids()
        if hasattr(model, 'get_user_type_names_and_ids'):
            # Dacă modelul are metoda aceasta, o folosim
            names_ids = model.get_user_type_names_and_ids()
            # Convertim la DataFrame
            import pandas as pd
            return pd.DataFrame(names_ids, columns=['ID', 'Name'])
        else:
            # Dacă nu, ridicăm eroare sau întoarcem ceva default
            raise NotImplementedError("Modelul nu are metoda get_user_type_names_and_ids")
