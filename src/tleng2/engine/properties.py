# have every not setting related variable stored here
# this file will be kept for legacy reasons, and for this module to be able to work as a framework, before it transitions into an engine
# TODO maybe we are going to move some functionality from here to their respective categories

import pygame
from .settings import GlobalSettings
from abc import abstractmethod, ABC

class LocalProperties(ABC):
    @abstractmethod
    def __init__(self):
        """
        Put the local specific properties that you want the scene/enviroment/object to have
        e.x. (pseudo code)

        self.fps = 30
        self.font = comic_sans
        self.disp = True
        self.in-game-keyboard = False
        """    


class EngineProperties:
    """
    Engine properties, needed across the framework/game.
    """
    _clock = pygame.time.Clock()
    _dt = 0
    _events = None
    _keys_pressed = None
    GAME_RUNNING = True

    # _index_event = 1

    # animation_database = {} # probably not to use


class SceneManagerProperties:
    _default_scene = ''

    _current_scene = ''
    
    _waiting_scene = ''
    _changing_scenes = False


class RendererProperties:
    __temp_disp = None

    _default_display = None

    _display = None
    _window = None

    _local_default_camera = None

    # parameters to be used in scenes
    scene_parameters = {}
    type_parameters = {}

    # when you call to render a sprite, it's renderable attr will be passed 
    # here for the renderer to later inspect it and render it
    render_calls = []