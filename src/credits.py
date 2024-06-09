"""
Credits scene class
"""
from .tleng2 import *
import pygame
import os


GAME_DIR = get_parent_dir(__file__, 2)

CREDITS = (
    os.path.join(GAME_DIR, 'assets','credits','Credits.png')
)

class Credits(Scene):
    def __init__(self,scene_name)->None:
        super().__init__(scene_name)

        self.credits_img = ImageService()
        self.credits_img.load_image(CREDITS,950,1750)
        self.credits_img.rect.centerx = GlobalSettings._disp_res[0]//2


    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            SceneManagerMethods.change_current_scene('Menu')
        
        scroll_y = self.credits_img.rect.centery

        for event in EngineProperties._events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: 
                    scroll_y = min(scroll_y + 30, 1750/2)
                    # print('up')
                if event.button == 5: 
                    scroll_y = max(scroll_y - 30, -1750/8)

        self.credits_img.rect.centery = scroll_y
    

    def update(self) -> None:
        self.credits_img.update()

    

    def render(self) -> None:
        RendererMethods.fill_display(color=colors.AQUA)
        self.credits_img.render()