import pygame
import pymunk
import sys

from src.tleng2 import *

from src.game import FreeRoam
from src.menu import Menu
from src.credits import Credits
# from src.tleng2.engine import EngineProperties


# DebugTags.import_tags()
GlobalSettings.update_bresolution((1280,720))
RendererMethods.load_displays()
EngineMethods.set_caption("PixelWheel")

GlobalSettings._debug = False
# GlobalSettings.load_settings_json()


if __name__ == '__main__':
    pygame.init()
    # initializing the scene classes
    free_roam = FreeRoam('FreeRoam')
    menu = Menu('Menu')
    credits = Credits('Credits')
    
    # updating the scene to menu
    SceneManagerMethods.change_current_scene("Menu")


    # running the game engine to run the game
    game = Game()
    game.run()