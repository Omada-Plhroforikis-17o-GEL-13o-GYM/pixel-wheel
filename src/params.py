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

from .tleng2 import RendererMethods
from .tleng2.components.camera import CameraCatcher


def import_params_needed() -> None:
    RendererMethods.import_scene_renderer_params_dict({
        'free_roam':{
            'display' : RendererMethods.load_local_display_ratio(1/3),
            'camera' : 'camera0'
        } 
    })