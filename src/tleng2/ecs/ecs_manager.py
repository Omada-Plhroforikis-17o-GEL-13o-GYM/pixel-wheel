from .scene import ECS_Scene


class ECS_Manager:
    def __init__(self) -> None:
        self.scenes: list[ECS_Scene] = []

