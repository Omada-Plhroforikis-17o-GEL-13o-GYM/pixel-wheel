import pygame
import pymunk
import sys
from src.tleng2 import *
# from tleng2.utils.debug import debug_print
# from src.tleng2.utils.debug import DebugTags
# from src.tleng2.utils.colors import RED, BLACK
pygame.init()

# DebugTags.import_tags()

GlobalSettings.update_bresolution((1280,720))
GlobalProperties.load_displays()
GlobalProperties.set_caption("PixelWheel")

GlobalSettings._debug = True
# GlobalSettings.load_settings_json()

camera = Camera()

class CarPlayer:
    def __init__(self) -> None:
        ...


class TestEnviroment(Scene):
    def __init__(self,scene_name)->None:
        super().__init__(scene_name)

        # self.space = pymunk.Space()


    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_w]:
            print("pressed w")
    

    def update(self) -> None:
        pass
    

    def render(self) -> None:
        # self.space.step(0.02) # 1/50 = 0.02, better pu the deltatime
        pass

if __name__ == '__main__':
    menu = TestEnviroment('Test_Enviroment')
    game = Game()
    SceneManager.current_scene = "Test_Enviroment"
    game.run()