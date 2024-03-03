"""
Scene handler
It justs puts the stuff on the screen and it handles the <scene changes> like menu->game->pause screen etc.
Idea:
SceneHandler will get layers, that the dev can assign multiple scenes to play.
Scene will just handle the updates of the objects that it draws. After they were updated and drawn to the buffer screen then they will be flipped and start again onto the next frame.
Scene should also change the scene state when neceasery.

SceneHandler should recognise the state of the app for the right scene to play.

Pseudo code:

class menu_scene ...
class game_scene ...

scene_dict = menu : menu_scene, game : game_scene  ...
game_state = menu

gameloop
    scene_phase(game_state)
    clock.tick(fps)
    buffer.flip()

fn scene_phase:
    sceneloop
        events()
        update()
        render()


"""
import pygame
from abc import ABC, abstractmethod
from ..utils.properties import GlobalProperties
from ..utils.settings import GlobalSettings
from ..utils.debug import debug_print


class SceneCatcher:
    scenes = {}

    def __init__(self, scene_key):
        self.scenes.update({scene_key: self})


class Scene(SceneCatcher, ABC):
    def __init__(self,scene_name)-> None:
        SceneCatcher.__init__(self,scene_key=scene_name)
        self.scene_name = scene_name

    @abstractmethod
    def event_handling(self, keys_pressed):
        '''
        To handle the events of mouse and other
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''

    @abstractmethod
    def update(self):
        '''
        game logic
        '''

    @abstractmethod
    def render(self):
        '''
        what to render to the screen
        '''


class SceneManager:
    """
    Manages like the animation service, scenes how they are getting rendered. Game Engine Backend function.
    """
    current_scene = ''

    def __init__(self, ) -> None: 
        """
        :param scenes: The dictionary should have Scene classes, or classes that have the structure of a scene class.
        :return: None
        """
        self.scenes = None
        # self.current_scene = ''
        self.layers = []


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
        GlobalProperties.update_window()
        GlobalProperties.clock_tick_GP_dt(GlobalSettings._fps)
        pygame.display.flip()


    def render_current_scene(self) -> None:
        """
        Renders the current scene that is assigned.
        """
        # for scene in SceneCatcher.scenes[self.current_scene]:
        scene = SceneCatcher.scenes[self.current_scene]
        keys_pressed = pygame.key.get_pressed()
        scene.event_handling(keys_pressed)
        scene.update()
        scene.render()
        pygame.display.flip()
        debug_print("Successfull scene render from SceneManager from SceneCatcher", tags=["Rendering"])


class SubSceneManagerCatcher:
    """
    Useful for split-screen gameplay were multiple scenemanagers might need to be used
    """
    ...


class SubSceneManager:
    ...


class SceneHandler:
    """
    Depracated, use Scene Manager instead!
    """
    def __init__(self):
        self.current_scene = ''

    def load_scenes(self, scenes):
        self.scenes = scenes
    
    def render_current_scene(self):
        for scene in SceneCatcher.scenes[self.current_scene]:
            scene.update_stuff()
            scene.render_stuff()
# the general idea that the scene can be controlled by the scene itself is kinda stupid.


# Scene grouping?
# Dictionary of scenes that upon render will be rendered the "current_scene, just like the animation"
# the whole idea is that the original scene is going to be created in another class, which will be stored here so the engine knows what to run.