# have every not setting related variable stored here
# this file will be kept for legacy reasons, and for this module to be able to work as a framework, before it transitions into an engine
# TODO maybe we are going to move some functionality from here to their respective categories

import pygame
from ..utils.settings import GlobalSettings
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
    
    # Temporary display variables
    __temp_disp = None
    
    _window = None # the window that you see
    _display = None # the inner display of the window
    _clock = pygame.time.Clock()
    _dt = 0
    _current_scene = 'default'

    # _index_event = 1

    # animation_database = {} # probably not to use

    @staticmethod
    def load_displays() -> None:
        """
        Initialize the displays quickly.
        """
        EngineProperties._display = pygame.Surface(GlobalSettings._disp_res) 
        EngineProperties._window = pygame.display.set_mode(GlobalSettings._win_res)


    @staticmethod
    def load_display() -> None:
        """
        Initialize the display.
        """
        EngineProperties._display = pygame.Surface(GlobalSettings._disp_res) 


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


    @staticmethod
    def set_caption(caption: str) -> None:
        pygame.display.set_caption(caption)


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
        EngineProperties._window.blit(EngineProperties._display, (0, 0))


    @staticmethod
    def fill_display(color: tuple[int, int, int]) -> None:
        """
        Fill the display with color.
        """
        EngineProperties._display.fill(color)
    
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
    

    @staticmethod
    def change_current_scene(new_scene: str) -> None:
        """
        Changes the value of the SceneManager in tleng2/core_engine/scene_manager.py
        """
        EngineProperties._current_scene = new_scene