"""
Settings scene class
"""
from dataclasses import dataclass

from tleng2.ecs.component import Component
from tleng2.ecs.world import World, Schedule
from tleng2.ecs.system import System, system

from tleng2 import *
from tleng2.components.camera import *


""" settings.py """

world = World()

@dataclass
class Coordinates2(Component):
    x: float
    y: float

@dataclass
class AreaComponent(Component):
    width: int
    height: int

@dataclass
class SpriteStackComponent(Component):
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


class AnimationSystem(System):
    def update(self):
        components = self.world.query(
            Coordinates2,
            optional = [
                AreaComponent
            ]
        )

        for coordinate in components:
            coordinate.x += 1
            coordinate.y += 1   

schedule = Schedule()

schedule.add_systems(
    AnimationSystem,
)




""" main.py """

# import setting_scene

# ecs_manager = ecs_manager()

# ecs_manager.add_scene(setting_scene)

# ecs_manager.set_current_scene(...)

""" ecs_manager """

# 