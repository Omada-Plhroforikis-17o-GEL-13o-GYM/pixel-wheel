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
Settings scene class
"""
from dataclasses import dataclass

from tleng2 import *
from tleng2.components.camera import *


""" settings.py """

world = ecs.World()

@dataclass
class Coordinates2:
    x: float
    y: float

@dataclass
class AreaComponent:
    width: int
    height: int

@dataclass
class SpriteStackComponent:
    dir_image_filepath: str


images_path = "path/to/spritestack"

camera = world.spawn(
    # CameraBundle()
)


# returns the id of the car 
car1 = world.spawn(
    Coordinates2(0,0),
    AreaComponent(10,10),
    SpriteStackComponent(images_path)
)

car2 = world.spawn(
    Coordinates2(5,5),
    AreaComponent(12,12),
    SpriteStackComponent(images_path + "2")
)

car3 = world.spawn(
    Coordinates2(5,5),
    AreaComponent(12,12),
)

car4 = world.spawn(
    Coordinates2(5,5),
    SpriteStackComponent(images_path + "2")
)



class AnimationSystem(ecs.System):
    def update(self):
        components = self.world.query(
            Coordinates2,

            has = (
                AreaComponent,
            )
        )

        print("Animation system", components)


class Test1System(ecs.System):
    def update(self):
        components = self.world.query(
            Coordinates2,
        )

        print("test1 system", components)


class Test2System(ecs.System):
    def update(self):

        print("test2 system")


class MovementSystem(ecs.System):
    def update(self):

        print("Doing Movement")


schedule = ecs.Schedule()

schedule.add_systems(
    AnimationSystem(5),
    Test1System(),
    MovementSystem(-2),
    Test2System(-3),
)

# print(schedule.system_schedule)

world.use_schedule(schedule)

world.run_schedule()
