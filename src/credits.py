"""
Credits scene class
"""
from .tleng2 import *
import pygame



class Credits(Scene):
    def __init__(self,scene_name)->None:
        super().__init__(scene_name)


    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            SceneManagerMethods.change_current_scene('Menu')
    

    def update(self) -> None:
        pass
    

    def render(self) -> None:
        RendererMethods.fill_display(color=colors.GOLD)