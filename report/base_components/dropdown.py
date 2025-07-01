import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from .base_component import BaseComponent
from fasthtml.common import Select, Label, Div, Option

class Dropdown(BaseComponent):


    def __init__(self, id="selector", name="user-selection", label="Choose the user"):
        self.id = id
        self.name = name
        self.label = label

    def build_component(self, entity_id, model):
        options = []
        for text, value in self.component_data(entity_id, model):
            option = Option(text, value=value, selected="selected" if str(value) == entity_id else "")
            options.append(option)


        dropdown_settings = {
            'name': self.name
            }

        # if model.name:
        #     dropdown_settings['disabled'] = 'disabled'

        selector = Select(
            *options,
            id=self.id,
            **dropdown_settings
            )

        return selector

    def outer_div(self, child):
        return Div(
            Label(self.label, **{"for": self.id}),
            child,
            id=self.id,
        )
