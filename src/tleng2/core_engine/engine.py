from .engine_properties import EngineProperties
from .scene_manager import SceneManager
from .renderer import Renderer
# from .ui_manager import UIManager

class GameEngine:
    def __init__(self) -> None:
        self.engine_properties = EngineProperties()
        self.d_renderer = Renderer()
        self.scene_manager = SceneManager()
        # abstractions

class GameEngine_exp:
    engine_properties = EngineProperties()
    d_renderer = Renderer()
    scene_manager = SceneManager()


game_engine = GameEngine()