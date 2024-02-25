import sys
import pygame
from .scene import SceneManager, SceneCatcher
from ..utils.debug import debug_print

class Game: 
    def __init__(self):
        # pygame.init()
        self.scene_manager1 = SceneManager()
        self.scene_manager2 = SceneManager()
        self.scene_manager3 = SceneManager()


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
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            self.scene_manager2.render_current_scene()
            debug_print(SceneCatcher.scenes, tags=["Rendering"])

        pygame.quit()
        sys.exit()


    