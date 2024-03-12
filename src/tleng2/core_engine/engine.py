# from abc import staticmethod
import pygame


class GameEngine():
    """
    On time classes should be initialized here, and for them to work, on the main game file.
    this should be runned:
    `tleng2.init_engine()`
    the initialization of the engine is going to run in the game class.
    """

    _clock = pygame.time.Clock()
    _dt = 0
    _current_scene = 'default'

    def __init__(self) -> None:

        ...

    @staticmethod
    def clock_tick_dt(target_fps: int) -> float:
        return GameEngine._clock.tick(target_fps) / 1000
        # return 1
    

    @staticmethod
    def clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in GameEngine.
        """
        GameEngine._dt = GameEngine._clock.tick(target_fps) / 1000


    # micro optimization
    @staticmethod
    def lazy_clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in GameEngine.
        """
        GameEngine._dt = GameEngine._clock.tick(target_fps) >> 10 # bit shift, clock.tick / 1024
    

    @staticmethod
    def change_current_scene(new_scene: str) -> None:
        """
        Changes the value of the SceneManager in tleng2/core_engine/scene_manager.py
        """
        GameEngine._current_scene = new_scene


def init_engine() -> None:
    ...