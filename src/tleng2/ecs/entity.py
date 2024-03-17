class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def remove_component(self, component_type):
        if component_type in self.components:
            del self.components[component_type]

    def has_component(self, component_type):
        return component_type in self.components

    def get_component(self, component_type):
        return self.components.get(component_type)