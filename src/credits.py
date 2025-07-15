# PixelWheel: Thessaloniki Edition - A pseudo 2.5D Racing game made in pygame 
# Copyright (C) 2024  theolaos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
        self.credits_img.frect.centerx = GlobalSettings._disp_res[0]//2


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