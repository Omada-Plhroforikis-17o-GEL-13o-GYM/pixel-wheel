"""
Gameplay scene class
"""
from .tleng2 import *
import pygame

class FreeRoam(Scene):
    def __init__(self,scene_name)->None:
        self.camera = Camera(default_camera=True)
        super().__init__(scene_name)
        
        # self.space = pymunk.Space()

    def scene_renderer_params(self) -> dict:
        parameters = {
            'camera' : self.camera.name,
            'display' : RendererMethods.load_local_display_ratio(1/2)
        }
        return parameters


    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            SceneManagerMethods.change_current_scene('Menu')


    def update(self) -> None:
        pass
    

    def render(self) -> None:
        RendererMethods.fill_display(color=colors.GRAY)