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
from ..engine.properties import EngineProperties
from ..engine.renderer import Renderer
from ..engine.settings import GlobalSettings
from ..utils.debug import debug_print


class SceneCatcher:
    scenes = {}

    def __init__(self, scene_key):
        self.scenes.update({scene_key: self})
        Renderer.scene_parameters.update({scene_key:self.scene_renderer_params()})



class Scene(SceneCatcher, ABC):
    def __init__(self,scene_name)-> None:
        SceneCatcher.__init__(self,scene_key=scene_name)
        self.scene_name = scene_name


    @abstractmethod
    def scene_renderer_params(self) -> dict:
        """
        This method needs to return a dictionary with certain parameters for the renderer
        """


    @abstractmethod
    def event_handling(self, keys_pressed) -> None:
        '''
        To handle the events of mouse and other
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''

    @abstractmethod
    def update(self) -> None:
        '''
        game logic
        '''

    @abstractmethod
    def render(self) -> None:
        '''
        what to render to the screen
        '''


class SubSceneManagerCatcher:
    """
    Useful for split-screen gameplay were multiple subscenemanagers might need to be used
    """
    ...


class SubSceneManager:
    ...


# the general idea that the scene can be controlled by the scene itself is kinda stupid.


# Scene grouping?
# Dictionary of scenes that upon render will be rendered the "current_scene, just like the animation"
# the whole idea is that the original scene is going to be created in another class, which will be stored here so the engine knows what to run.