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
import sys

from src.tleng2 import * 
from src.tleng2.utils.debug import DebugTags

from src.game import FreeRoam
from src.menu import Menu
from src.credits import Credits
from src.loader import LoadingScene

from src.params import import_params_needed
# from src.tleng2.engine import EngineProperties

GlobalSettings.update_resolutions((1280,720),(1280,720))
RendererMethods.load_displays()
EngineMethods.set_caption("PixelWheel: Thessaloniki Edition")

assets_dir = ""

if getattr(sys, 'frozen', False):
    base_path = sys.executable
    assets_dir = os.path.join(get_parent_dir(__file__, 2), 'assets')
else:
    assets_dir = os.path.join(os.path.abspath("."), "assets")

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

GlobalSettings._debug = False
DebugTags.import_tags([
    'HITBOXES', 
    'POINTS',
    # 'RENDERABLE_RECT',
    # 'renderer', 
    # 'image_service'
])
# GlobalSettings.load_settings_json()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    # initializing the scene classes

    game = App()
    LoadingScene([
        (Menu, 'Menu'),
        (FreeRoam, 'FreeRoam'),
        (Credits, 'Credits'),
    ]).run()
    # updating the scene to menu
    SceneManagerMethods.start_with_scene("Menu")
    
    # running the game engine to run the game
    game.run_old()

"""
PERF TODO:
Rendering every spritestack in a single surface inside a chunk. (if spritestack is static, ex in the map)
and caching the whole chunk in the caches of the spritestack instead of seperate ones. if one spritestck in a stack
dont cache.

QOL TODO:
Nodify the scene manager.

Abolish the catchers.
"""