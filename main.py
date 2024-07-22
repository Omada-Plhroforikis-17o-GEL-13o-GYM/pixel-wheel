import pygame
import os
import json

from src.tleng2 import * 
from src.tleng2.utils.debug import DebugTags

from src.game import FreeRoam
from src.menu import Menu
from src.credits import Credits

# from src.credits import world as CreditsScene
# from src.settings import world as SettingsScene

from src.params import import_params_needed
# from src.tleng2.engine import EngineProperties


# DebugTags.import_tags()
GlobalSettings.update_bresolution((1280,720))
# GlobalSettings._debug = True
# DebugTags.import_tags(['renderable'])
RendererMethods.load_displays()
EngineMethods.set_caption("PixelWheel: Thessaloniki Edition")

assets_dir = os.path.join(get_parent_dir(__file__, 1), 'assets')
fps = 60
try:
    with open(os.path.join(assets_dir, 'settings.json'),'r') as settings:
        print(settings)
        fps = json.load(settings)['FPS']
except Exception as error:
    print("FPS ERROR FILE/TAG NOT FOUND")
    print(error)
    fps = 60
GlobalSettings._fps = fps
# EngineMethods.import_render_params(`file`) the file is .json
import_params_needed()

GlobalSettings._debug = False
# GlobalSettings.load_settings_json()


if __name__ == '__main__':
    pygame.init()
    # initializing the scene classes

    game = Game()

    # game.load_worlds(
    #     FreeRoam(), 
    #     Menu(), 
    #     Credits(),
    #     settings()
    # )
    free_roam = FreeRoam('FreeRoam')
    menu = Menu('Menu')
    credits = Credits('Credits')
    
    # updating the scene to menu
    SceneManagerMethods.start_with_scene("FreeRoam")
    
    # running the game engine to run the game
    game.run()

"""
TODO:
Redo the coordinate system. The world coordinates should be independent from the screen coordinates.

Independent Coordinates even in different screen sizes.

Redo the tilemaps.

Add multiworld entities?
(a new actual reason for the world manager to exist)
Ans: better ways of storing and loading maps. in a single scene.

PERF TODO:
Rendering every spritestack in a single surface inside a chunk.

QOL TODO:
Change the debug print class/functions to a logger.

Nodify the scene manager.

Abolish the catchers.

"""