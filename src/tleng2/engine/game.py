import sys
import os
import pygame

from ..engine.properties import EngineProperties, SceneManagerProperties, RendererProperties
from ..engine.methods import  EngineMethods, RendererMethods, SceneManagerMethods
from ..engine.renderer import Renderer
from ..components.scene import SceneCatcher
from ..utils.debug import debug_print
from .settings import GlobalSettings
from .scene_manager import SceneManager




class Game: 
    def __init__(self):
        # pygame.init()
        self.scene_manager = SceneManager()
        self.renderer = Renderer()
        

    def run(self, tleng2_intro: bool = True):
        '''
        to play the game
        '''
        
        if tleng2_intro:
            pass

        EngineProperties.GAME_RUNNING = True
        while EngineProperties.GAME_RUNNING:
            # handle the scene from here
            events = pygame.event.get()
            EngineProperties._events = events
            
            for event in events:
                if event.type == pygame.QUIT: # escape to exit, personal preference
                    pygame.quit()
                    sys.exit()

            self.scene_manager.render_current_scene()
            self.renderer.render()
            RendererMethods.update_window()
            pygame.display.flip()

            RendererMethods.clear_render_calls()
            EngineMethods.clock_tick_GP_dt(GlobalSettings._fps)
            SceneManagerMethods.update_scene()

            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()


    