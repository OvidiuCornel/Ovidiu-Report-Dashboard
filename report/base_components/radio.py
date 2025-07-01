from .base_component import BaseComponent
from fasthtml.common import Input, Label, Div, Fragment

class Radio(BaseComponent):
    def __init__(self, name, model=None, value=None, hx_get=None, hx_target=None, values=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name      = name
        self.model     = model
        self.value     = value
        self.hx_get    = hx_get
        self.hx_target = hx_target
        self.values    = values or []

    def build_component(self, entity_id=None, model=None, *args, **kwargs):
        self.model = model or self.model

        # obținem lista de valori (tuple sau simple)
        source_values = self.values or self.model.names()

        radios = []
        for item in source_values:
            # extragem string‑ul de afișat
            label_text = item[1] if isinstance(item, tuple) else item
            input_id   = (item[0] if isinstance(item, tuple) else item) \
                           .lower().replace(" ", "-")
            is_checked = "checked" if (label_text == self.value) else ""

            # pentru fiecare radio, creăm <label><input … /> Text</label>
            radios.append(
                Label(
                    Fragment(
                        Input(
                            type="radio",
                            id=input_id,
                            name=self.name,
                            value=label_text,
                            hx_get=self.hx_get,
                            hx_target=self.hx_target,
                            hx_trigger="change",
                            checked=is_checked
                        ),
                        label_text
                    ),
                    **{"for": input_id}
                )
            )

        # Le putem grupa într‑un <div> dacă vrei
        return Div(*radios, cls="radio-group")
