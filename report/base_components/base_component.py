from fasthtml.common import Div  # importul corect

class BaseComponent:
    def __init__(self, components=None):
        self.components = components or []

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
