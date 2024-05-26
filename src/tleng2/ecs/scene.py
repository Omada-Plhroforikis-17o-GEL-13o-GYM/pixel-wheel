from .system import System
from .entity import Entity


class ECS_Scene:
    def __init__(self) -> None:
        self.entities: list[Entity] = []

        self.systems: list[System] = []

        self.explicit_systems: list[System] = []


    # i don't really like this code
    def add_entities(self, *entities: Entity) -> None:
        self.entities += entities


    # i don't really like this code
    def add_systems(self, *systems: System) -> None:
        self.systems += systems


    def use_systems(self, *systems: System) -> None:
        self.systems = systems