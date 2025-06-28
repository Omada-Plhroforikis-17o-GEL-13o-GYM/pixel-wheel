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

EngineMethods.set_icon(os.path.join(assets_dir, 'logo', 'pixel_wheel_whole_logo.png'))
fps = 60
try:
    with open(os.path.join(assets_dir, 'settings.json'),'r') as settings:
        print(settings)
        fps = json.load(settings)['FPS']
except Exception as error:
    print("FPS ERROR FILE/TAG NOT FOUND")
    print(error)
    
GlobalSettings._fps = fps
# EngineMethods.import_render_params(`file`) the file is .json
import_params_needed()

GlobalSettings._debug = True
# GlobalSettings.load_settings_json()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    # initializing the scene classes

    game = App()

    FreeRoam('FreeRoam')
    Menu('Menu')
    Credits('Credits')
    
    # updating the scene to menu
    SceneManagerMethods.start_with_scene("Menu")
    
    # running the game engine to run the game
    game.run_old()

"""
TODO:
Redo the coordinate system. The world coordinates should be independent from the screen coordinates.

Independent Coordinates even in different screen sizes.

PERF TODO:
Rendering every spritestack in a single surface inside a chunk. (if spritestack is static, ex in the map)
and caching the whole chunk in the caches of the spritestack instead of seperate ones. if one spritestck in a stack
dont cache.

QOL TODO:
Change the debug print class/functions to a logger.

Nodify the scene manager.

Abolish the catchers.

"""