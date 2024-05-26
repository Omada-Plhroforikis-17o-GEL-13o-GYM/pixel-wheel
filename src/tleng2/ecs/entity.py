class IEntity: ... # id entity


class Entity:
    def __init__(self, **components):
        self.components = {}

        if components != []:
            for component in components:
                self.add_component(component)

    def add_component(self, component):
        self.components[type(component)] = component

    def remove_component(self, component_type):
        if component_type in self.components:
            del self.components[component_type]

    def has_component(self, component_type):
        return component_type in self.components

    def get_component(self, component_type):
        return self.components.get(component_type)