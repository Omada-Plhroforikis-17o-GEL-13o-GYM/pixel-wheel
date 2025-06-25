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


import math
import pymunk
import pygame
import os
import json
from pygame import Vector2
from pymunk import Vec2d

from .physics import Player, Wall
from .tleng2 import *

def rotate_to_center(rot: float, pos: tuple[float, float], center: tuple[float, float]) -> tuple[float, float]:
    """
    Angle in radians
    """
    
    vec_x = pos[0] -  center[0]
    vec_y = pos[1] - center[1]

    new_x = math.cos(rot)*vec_x + math.sin(rot)*vec_y
    new_y = -math.sin(rot)*vec_x + math.cos(rot)*vec_y

    return (new_x, new_y)

def flipy(p):
    """Convert chipmunk coordinates to pygame screen coordinates."""
    return Vector2(p[0], -p[1]+RendererProperties._display.get_size()[1])


def convert_to_vector2(p):
    """Convert chipmunk coordinates to pygame vector2"""
    return Vector2(p[0], p[1])


def flipy_pymunk(p) -> float:
    """."""
    return Vec2d(p[0], -p[1]+RendererProperties._display.get_size()[1])


def image_load(*path) -> pygame.Surface:
    return pygame.image.load(os.path.join(*path)).convert_alpha()


def rect_to_vertices(rect) -> list[Vector2]:
    return [Vec2d(*rect.topleft), Vec2d(*rect.topright), Vec2d(*rect.bottomright), Vec2d(*rect.bottomleft)]


def transformation(ss: SpriteStackService, transform: Camera.get_transform) -> None:
    """
    ss: SpriteStackService
    transform: Camera.get_transform function
    """
    vec = transform(Vector2(ss.world_pos[0], ss.world_pos[1]))
    ss.update({'x': vec.x, 'y': vec.y})


class FreeRoam(Scene):
    def __init__(self, scene_name) -> None:
        self.camera = Camera(default_camera = True)
        self.camera_run_setup = False
        # self.camera.
        super().__init__(scene_name,'free_roam')
        assets_dir = os.path.join(get_parent_dir(__file__,2), 'assets')

        self.angle = 0 #radians
        
        self.debug = True

        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        self.space.damping = .01

        self.player_sprite = SpriteStackService()
        self.player_sprite.renderable.centered = True
        car = 'RED'
        try:
            with open(os.path.join(assets_dir, 'settings.json'),'r') as settings:
                print(settings)
                car = json.load(settings)['CAR']
        except Exception as error:
            print(error)
            car = 'RED'
            
        try:
            self.player_sprite.load_images(os.path.join(assets_dir,car))
        except:
            self.player_sprite.load_images(os.path.join(assets_dir,'RED'))

        self.player = Player((200,-100), self.space, 1, self.player_sprite.images[0].get_width(),self.player_sprite.images[0].get_height())

        # print(self.player_sprite.images[0].get_width(),self.player_sprite.images[0].get_height())

        

        # tileset should import from a .json file as well.
        self.city_streets_tileset = TileSet({
            'road_straight_up' : image_load(assets_dir,'city_tileset', 'road_straight_up.png'),
            'road_straight_down' : image_load(assets_dir,'city_tileset', 'road_straight_down.png'),
            'road_straight_right' : image_load(assets_dir,'city_tileset', 'road_straight_right.png'),
            'road_straight_left' : image_load(assets_dir,'city_tileset', 'road_straight_left.png'),
            'road_turn_ne' : image_load(assets_dir,'city_tileset','road_turn_ne.png'),
            'road_turn_se' : image_load(assets_dir,'city_tileset','road_turn_se.png'),
            'road_turn_sw' : image_load(assets_dir,'city_tileset','road_turn_sw.png'),
            'road_turn_nw' : image_load(assets_dir,'city_tileset','road_turn_nw.png'),
            'pavement' : image_load(assets_dir,'city_tileset', 'pavement.png'),
            'road' : image_load(assets_dir,'city_tileset', 'road.png'),
            'paved_road' : image_load(assets_dir,'city_tileset', 'paved_road.png')
        }, 35, 35)

        RU = 'road_straight_up'
        RD = 'road_straight_down'
        RR = 'road_straight_right'
        RL = 'road_straight_left'
        NE = 'road_turn_ne'
        SE = 'road_turn_se'
        SW = 'road_turn_sw'
        NW = 'road_turn_nw'
        PO = 'pavement'
        RO = 'road'
        PR = 'paved_road'


        tilemap = [
            [RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO],
            [RO,SE,RD,RD,RD,SW,SE,RD,RD,RD,SW,RO,RO],
            [RO,RR,PO,PO,PO,RL,RR,PO,PO,PO,RL,RO,RO],
            [RO,RR,PO,PO,PO,RL,NE,RU,RU,RU,NW,RO,RO],
            [RO,RR,PO,PO,PO,RL,SE,RD,RD,RD,SW,RO,RO],
            [RO,NE,RU,RU,RU,NW,NE,RU,RU,RU,NW,RO,RO],
            [RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO],
            [RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO],
            [RO,SE,RD,RD,RD,SW,SE,RD,RD,RD,SW,RO,RO],
            [RO,RR,PO,PO,PO,RL,RR,PO,PO,PO,RL,RO,RO],
            [RO,RR,PO,PO,PO,RL,NE,RU,RU,RU,NW,RO,RO],
            [RO,RR,PO,PO,PO,RL,SE,RD,RD,RD,SW,RO,RO],
            [RO,NE,RU,RU,RU,NW,NE,RU,RU,RU,NW,RO,RO],
            [RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO],            
        ]


        ht = 35/2
        dc = 4 # distance from curb y px
        
        self.tile_hitboxes = {
            'road_straight_up' : rect_to_vertices(pygame.FRect(-ht, ht-dc, ht*2, dc)), # done
            'road_straight_down' : rect_to_vertices(pygame.FRect(-ht, -ht, ht*2, dc)), # done
            'road_straight_right' : rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, ht*2)), # done
            'road_straight_left' : rect_to_vertices(pygame.FRect(-ht, -ht, dc, ht*2)), # done
            'road_turn_ne' : rect_to_vertices(pygame.FRect(ht-dc, ht-dc, dc, dc)), # done
            'road_turn_se' : rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, dc)),
            'road_turn_sw' : rect_to_vertices(pygame.FRect(-ht, -ht, dc, dc)), # done
            'road_turn_nw' : rect_to_vertices(pygame.FRect(-ht, ht-dc, dc, dc)), # done
            'pavement' : rect_to_vertices(pygame.FRect(-ht, -ht, ht*2, ht*2)),
        }

        no_hitbox = ['road', 'paved_road']

        for y, y_tiles in enumerate(tilemap):
            for x, tile_name in enumerate(y_tiles):
                if tile_name in no_hitbox:
                    continue
                else:
                    # Wall((x*35+35/2+1,-y*35+129), self.tile_hitboxes[tile_name],self.space, 1)
                    Wall((x*35,-y*35), self.tile_hitboxes[tile_name],self.space, 1)
                

        tile_size = 35/2

        self.free_roam_tilemap = Map()
        self.free_roam_tilemap.load_tilemap(tilemap)
        self.free_roam_tilemap.load_tileset(self.city_streets_tileset)
        self.free_roam_tilemap.pre_render()
        self.free_roam_tilemap.center

        RO = 'ROTONTA'
        LE = 'LEFKOS'
        BU = 'building'
        LL = "none"

        sprite_stack_tilemap = [
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,RO,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LE,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],              
        ]

        self.rotonta = SpriteStackService()
        self.rotonta.load_images(os.path.join(assets_dir,'ROTONTA'))
        self.rotonta.update({'x':tile_size*7,'y':tile_size*7})

        self.lefkos_pirgos = SpriteStackService()
        self.lefkos_pirgos.load_images(os.path.join(assets_dir,'LEFKOS'))
        self.lefkos_pirgos.update({'x':tile_size*7,'y':35*10+15})


        self.polikatikia1 = SpriteStackService()
        self.polikatikia1.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia1.update({'x':tile_size*9,'y':tile_size*19})
        # self.polikatikia1.spread = 35

        self.polikatikia2 = SpriteStackService()
        self.polikatikia2.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia2.update({'x':tile_size*5,'y':tile_size*5})

        self.polikatikia3 = SpriteStackService()
        self.polikatikia3.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia3.update({'x':tile_size*19,'y':tile_size*5})

        self.polikatikia4 = SpriteStackService()
        self.polikatikia4.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia4.update({'x':tile_size*9,'y':tile_size*7})

        self.polikatikia5 = SpriteStackService()
        self.polikatikia5.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia5.update({'x':tile_size*17,'y':tile_size*19})

        self.polikatikia6 = SpriteStackService()
        self.polikatikia6.load_images(os.path.join(assets_dir,'building'))
        self.polikatikia6.update({'x':tile_size*5,'y':tile_size*19})

        self.buildings = [
            self.polikatikia5,
            self.polikatikia1,
            self.polikatikia2,
            self.polikatikia3,
            self.polikatikia4,
            self.polikatikia6
        ]

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)


        # self.space = pymunk.Space()

    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            self.camera_run_setup = False
            SceneManagerMethods.change_current_scene('Menu')
        for event in EngineProperties._events:
            self.player.handle_event(event)

        if keys_pressed[pygame.K_LEFT]:
            self.angle += 0.01
        if keys_pressed[pygame.K_RIGHT]:
            self.angle -= 0.01


    def update(self) -> None:
        if not self.camera_run_setup:
            self.camera.update_center_screen((RendererProperties._display.get_width()/2, RendererProperties._display.get_width()/2))
            self.camera_run_setup = True
        
        self.space.step(EngineProperties._dt)

        self.player.update(EngineProperties._dt)

        pos = convert_to_vector2(self.player.body._get_position())

        # When rewriting, this can be optimized
        self.camera.update_center((pos.x,pos.y))
        
        self.player_sprite.update_new(
            x = pos.x,
            y = pos.y,
        )
        # self.player_sprite.update_new(
        #     x = int(self.camera.offset_pos.x + RendererProperties._display.get_width()//2),
        #     y = int(self.camera.offset_pos.y + RendererProperties._display.get_height()//2),
        # )

        EngineMethods.set_caption(f"{EngineProperties._clock.get_fps():.2f}")

        # print(angl,self.player.body._get_angle())

        # self.rotonta.update({'x':35,'y':50})
        # self.lefkos_pirgos.update()
    

    def render(self) -> None:
        RendererMethods.fill_display(color=(34,32,52))

        # Center of rotation is the player's position
        player_pos = convert_to_vector2(self.player.body._get_position())

        transform = self.camera.get_transform()

        # Render the tilemap with rotation around the player
        self.free_roam_tilemap.render_angle(
            convert_rad_to_deg(self.angle),
        )

        # Render all world objects (buildings, etc.) rotated around the player
        for building in self.buildings:

            building.render(self.angle)

        # Render landmarks
        self.rotonta.render(self.angle)

        self.lefkos_pirgos.render(self.angle)

        # Render the player sprite at the center of the screen, only with its own angle
        self.player_sprite.rotation = convert_rad_to_deg(self.player.body.rotation_vector.angle)
        self.player_sprite.render()

        print(f"Player world position: {player_pos}")

        # Draw direction line
        velocity = Vector2(0,1).rotate_rad(-self.player.body.rotation_vector.angle)
        if velocity.length() > 0:
            velocity_dir = velocity.normalize() * 50  # Length of the line
            start_screen = Vector2(RendererProperties._display.get_width() // 2, RendererProperties._display.get_height() // 2)
            end_screen = start_screen + velocity_dir
            pygame.draw.line(RendererProperties._display, (255, 0, 0), start_screen, end_screen, 3)
