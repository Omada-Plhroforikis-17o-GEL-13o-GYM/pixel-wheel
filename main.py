import pygame
import pymunk
import sys

from src.tleng2 import *
# from src.tleng2.engine import EngineProperties


# DebugTags.import_tags()

GlobalSettings.update_bresolution((1280,720))
GlobalProperties.load_displays()
EngineProperties.set_caption("PixelWheel")

EngineProperties._debug = False
# GlobalSettings.load_settings_json()


camera = Camera(default_camera=True)

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
    pygame.init()
    menu = TestEnviroment('Test_Enviroment')
    game = Game()
    GlobalProperties.change_current_scene("Test_Enviroment")
    game.run()