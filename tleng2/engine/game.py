import sys
import pygame
from .scene import SceneManager

# _______________________________________________________ Game Engine __________________________________________________________

class Game: 
    def __init__(self,scenes):
        # pygame.init()
        self.scenes = SceneManager(scenes)


    def run(self, tleng2_intro:bool=True):
        '''
        to play the game
        '''
        if tleng2_intro:
            pass

        self.running = True
        while self.running:
            # handle the scene from here
            self.scenes.scene_phase()

        pygame.quit()
        sys.exit()


    