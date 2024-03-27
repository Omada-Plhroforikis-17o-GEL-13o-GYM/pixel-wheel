from .event_bus import Subscriber
from .properties import SceneManagerProperties, RendererProperties


class RendererPropertiesUpdater(Subscriber):
    def __init__(self) -> None:
        super().__init__(self)


    def receive(self, message) -> None:
        ...    


class SceneManagerPropertiesUpdater(Subscriber):
    def __init__(self) -> None:
        super().__init__(self)


    def receive(self, message) -> None:
        SceneManagerProperties._current_scene = SceneManagerProperties._current_scene