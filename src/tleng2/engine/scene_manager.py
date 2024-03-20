from ..components.scene import Scene, SceneCatcher
from .settings import GlobalSettings
from ..utils.debug import debug_print
from .properties import EngineProperties
import pygame

class SceneManager:
    """
    Manages the animation service, scenes how they are getting rendered. Game Engine Backend function.
    """

    def __init__(self, ) -> None: 
        """
        :param scenes: The dictionary should have Scene classes, or classes that have the structure of a scene class.
        :return: None
        """
        self.scenes = None
        self.scene_layers = [] # future support for having a scene render on top of another scene, 

        # self.current_scene = ''

    def return_scene_phase(self, key:str) -> Scene:
        """
        Returns the entire scene class.
        :param key: Must be a string
        :return: Scene Class
        """
        return self.scenes[key]
    

    def load_scenes(self, scenes: dict[str,Scene]) -> None:
        self.scenes = scenes
    

    @staticmethod
    def rendering_scene(scene):
        pygame.event.pump()
        keys_pressed = pygame.key.get_pressed()
        scene.event_handling(keys_pressed)
        scene.update()
        scene.render()
        EngineProperties.update_window()
        EngineProperties.clock_tick_GP_dt(GlobalSettings._fps)
        pygame.display.flip()

    @staticmethod
    def render_current_scene() -> None:
        """
        Renders the current scene that is assigned.
        """
        # for scene in SceneCatcher.scenes[self.current_scene]:
        scene = SceneCatcher.scenes[EngineProperties._current_scene]
        keys_pressed = pygame.key.get_pressed()
        scene.event_handling(keys_pressed)
        scene.update()
        scene.render()
        pygame.display.flip()

        debug_print("Successfull scene render from SceneManager from SceneCatcher", tags=["Rendering"])