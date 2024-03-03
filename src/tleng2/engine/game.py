import sys
import pygame
from .scene import SceneCatcher
from ..utils.debug import debug_print
from ..utils.properties import GlobalProperties
from ..utils.settings import GlobalSettings
from ..core_engine.scene_manager import SceneManager


class Game: 
    def __init__(self):
        # pygame.init()
        self.scene_manager = SceneManager()


    def run(self, tleng2_intro: bool = True):
        '''
        to play the game
        '''

        if tleng2_intro:
            pass

        self.running = True
        while self.running:
            # handle the scene from here
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # escape to exit, personal preference
                    pygame.quit()
                    sys.exit()
            self.scene_manager.render_current_scene()
            GlobalProperties.update_window()
            GlobalProperties.clock_tick_GP_dt(GlobalSettings._fps)
            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()


    