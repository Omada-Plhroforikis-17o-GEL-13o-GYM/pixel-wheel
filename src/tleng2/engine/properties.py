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
    _current_scene = 'default'

    # _index_event = 1

    # animation_database = {} # probably not to use


class SceneManagerProperties:
    _current_scene = ''


class RendererProperties:
    scene_parameters = {}

    __temp_disp = None

    _display = None
    _window = None

    # when you call to render a sprite, it's renderable attr will be passed 
    # here for the renderer to later inspect it and render it
    render_calls = []


class EngineMethods:
    @staticmethod
    def set_caption(caption: str) -> None:
        pygame.display.set_caption(caption)

    
    @staticmethod
    def clock_tick_dt(target_fps: int) -> float:
        return EngineProperties._clock.tick(target_fps) / 1000
        # return 1
    

    @staticmethod
    def clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) / 1000


    # micro optimization
    @staticmethod
    def lazy_clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) >> 10 # bit shift, clock.tick / 1024
    

class SceneManagerMethods:
    """
    SceneManager Static methods that might be needed across the base game.
    """
    @staticmethod
    def change_current_scene(new_scene: str) -> None:
        """
        Changes the value of the SceneManager in tleng2/core_engine/scene_manager.py
        """
        SceneManagerProperties._current_scene = new_scene


class RendererMethods:
    """
    Renderer Static methods that might be needed across the base game.
    """
    @staticmethod
    def clear_render_calls():
        RendererProperties.render_calls = []


    @staticmethod
    def lazy_upscale_display(new_res: tuple[int,int] = GlobalSettings._win_res) -> None:
        """
        Scaling the display to the size of the window.
        And updates the window with the upscale.
        Warning may be very pixelated.
        """
        EngineProperties.__temp_disp = pygame.transform.scale(EngineProperties._display, new_res)
        EngineProperties._window.blit(EngineProperties.__temp_disp, (0, 0))


    @staticmethod
    def update_window() -> None:
        """
        Updates the window from _display immedietely.
        """
        RendererProperties._window.blit(RendererProperties._display, (0, 0))

    @staticmethod
    def fill_display(color: tuple[int, int, int]) -> None:
        """
        Fill the display with color.
        """
        EngineProperties._display.fill(color)

    @staticmethod
    def load_window(
            flags: int = 0,
            depth: int = 0,
            display: int = 0,
            vsync: int = 0
        ) -> None:
        """
        Initialize the window, with added parameters.
        """
        EngineProperties._window = pygame.display.set_mode(GlobalSettings._win_res, flags, depth, display, vsync) 