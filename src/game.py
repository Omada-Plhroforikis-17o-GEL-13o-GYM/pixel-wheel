"""
Gameplay scene class
"""
from .tleng2 import *
from .physics import Player
import pygame




class FreeRoam(Scene):
    def __init__(self,scene_name)->None:
        self.camera = Camera(default_camera=True)
        super().__init__(scene_name,'free_roam')

        self.player = Player()
        self.tileset = None
        self.tilemap = None

        # self.space = pymunk.Space()

    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            SceneManagerMethods.change_current_scene('Menu')


    def update(self) -> None:
        pass
    

    def render(self) -> None:
        RendererMethods.fill_display(color=colors.GRAY)