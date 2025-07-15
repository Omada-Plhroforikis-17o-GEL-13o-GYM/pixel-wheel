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
Menu scene class
"""
import os
import pygame
import json

from .tleng2 import *

pygame.init()


def play_callback():
    SceneManagerMethods.change_current_scene('FreeRoam')

def credits_callback():
    SceneManagerMethods.change_current_scene('Credits')

GAME_DIR = get_parent_dir(__file__, 2)


LOGO = (
    os.path.join(GAME_DIR, 'assets',"logo",'WholeLogoWithText.png')
)

PLAY_BUTTON_IMG = (
    os.path.join(GAME_DIR, 'assets',"buttons",'play','play_0001.png'),
    os.path.join(GAME_DIR, 'assets',"buttons",'play','play_0002.png'),
    os.path.join(GAME_DIR, 'assets',"buttons",'play','play_0003.png'),
)

CREDITS_BUTTON_IMG = (
    os.path.join(GAME_DIR, 'assets',"buttons",'credits','credits_0001.png'),
    os.path.join(GAME_DIR, 'assets',"buttons",'credits','credits_0002.png'),
    os.path.join(GAME_DIR, 'assets',"buttons",'credits','credits_0003.png'),    
)

BG_MUSIC = pygame.mixer.Sound(
    os.path.join(GAME_DIR,'assets','music','bg_music.wav')
)

MUSIC_VOLUME = 0.2
try:
    with open(os.path.join(GAME_DIR, "assets", 'settings.json'),'r') as settings:
        print(settings)
        MUSIC_VOLUME = json.load(settings)['MUSIC_VOLUME']
except Exception as error:
    print(error)
    print("MUSIC ERROR FILE/TAG NOT FOUND")
    MUSIC_VOLUME = 0.2


class Menu(Scene):
    def __init__(self,scene_name) -> None:
        super().__init__(scene_name)
        self.play_button_cords = pygame.FRect(0,400,200,80)
        self.play_button_cords.centerx = GlobalSettings._disp_res[0]/2
        self.play_button = Button(
                                self.play_button_cords.x,
                                self.play_button_cords.y,
                                'play',
                                self.play_button_cords.width,
                                self.play_button_cords.height,
                                PLAY_BUTTON_IMG,
                                callback=play_callback
                            )

        self.credits_button_cords = pygame.FRect(0,500,200,80)
        self.credits_button_cords.centerx = GlobalSettings._disp_res[0]/2
        self.credits_button = Button(
                                self.credits_button_cords.x,
                                self.credits_button_cords.y,
                                'play',
                                self.credits_button_cords.width,
                                self.credits_button_cords.height,
                                CREDITS_BUTTON_IMG,
                                callback=credits_callback
                            )
        
        self.image = ImageService()
        scalar = 7
        self.image.load_image(LOGO, 57*scalar, 57*scalar)
        self.image.frect.centerx = GlobalSettings._disp_res[0]/2 - 10
        self.image.frect.centery = 230

        BG_MUSIC.play(-1)
        BG_MUSIC.set_volume(MUSIC_VOLUME)


    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            print('you pressed escape')
        self.play_button.handle_event()
        self.credits_button.handle_event()

    

    def update(self) -> None:
        self.image.update()
    

    def render(self) -> None:
        RendererMethods.fill_display(color=colors.AQUA)
        self.play_button.simple_draw()
        self.credits_button.simple_draw()
        self.image.render()


# pixel
#  wheel