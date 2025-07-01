
# report/combined_components/combined_component.py

from report.base_components.base_component import BaseComponent
from report.base_components.dropdown import Dropdown
from report.base_components.data_table import DataTable
from report.base_components.matplotlib_viz import LineChart, BarChart
from report.base_components.radio import Radio

from fasthtml.common import Div
from fastcore.xml import FT


class BaseComponent:
    def build_component(self, entity_id, model):
        raise NotImplementedError

    def outer_div(self, component, div_args=None):
        if div_args is None:
            div_args = {}
        return Div(component, **div_args)

    def component_data(self, entity_id, model):
        raise NotImplementedError

    def __call__(self, entity_id, model):
        component = self.build_component(entity_id, model)
        return self.outer_div(component)


class FormGroup(BaseComponent):
    def __init__(self, label=None, components=None):
        self.components = components or []
        self.label = label

    def build_component(self, entity_id, model):
        form_items = []
        for comp in self.components:
            form_items.append(comp(entity_id, model))
        return Div(*form_items)

    def outer_div(self, component, div_args=None):
        if div_args is None:
            div_args = {}
        # adaugă clasa form-group în argumentele Div
        div_args.setdefault("class_", "form-group")
        return super().outer_div(component, div_args)

class CombinedComponent(BaseComponent):
    def __init__(self, components=None):
        self.components = components or []
        super().__init__()

    outer_div_type = Div(cls='container')

    def __call__(self, userid, model):

       called_children = self.call_children(userid, model)
       div_args = self.div_args(userid, model)

       return self.outer_div(called_children, div_args)

    def call_children(self, userid, model):

        called = []
        for child in self.children:
            if isinstance(child, FT):
                called.append(child())

            else:
                called.append(child(userid, model))

        return called

    def div_args(self, userid, model):
        return {}

    def outer_div(self, children, div_args):

        self.outer_div_type.children = ()

        return self.outer_div_type(
            *children,
            **div_args
        )
