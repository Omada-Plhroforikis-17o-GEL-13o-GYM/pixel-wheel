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
    with open(os.path.join(GAME_DIR, 'settings.json'),'r') as settings:
        print(settings)
        MUSIC_VOLUME = json.load(settings)['MUSIC_VOLUME']
except Exception as error:
    print(error)
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
        scalar = 5
        self.image.load_image(LOGO, 57*scalar, 32*scalar)
        self.image.rect.centerx = GlobalSettings._disp_res[0]/2
        self.image.rect.y = 200

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
