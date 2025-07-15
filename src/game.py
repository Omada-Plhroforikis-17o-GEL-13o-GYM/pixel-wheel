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
from .tleng2.utils.debug import DebugTags

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

def lerp_angle(a, b, t):
    """Linearly interpolate from angle a to b by t, handling wraparound."""
    diff = (b - a + math.pi) % (2 * math.pi) - math.pi
    return a + diff * t


def wall_visualization(wall: Wall, color: tuple[int, int, int, int] = (0,255,255,100)) -> pygame.Surface:
    # --- Create a renderable for this wall ---
    # Get vertices in world coordinates
    verts = [wall.body.local_to_world(v) for v in wall.shape.get_vertices()]
    # Convert to pygame coordinates
    verts_pg = [ Vector2(v.x, v.y) for v in verts]
    # Find bounding rect
    min_x = min(v.x for v in verts_pg)
    min_y = min(v.y for v in verts_pg)
    max_x = max(v.x for v in verts_pg)
    max_y = max(v.y for v in verts_pg)
    width = max_x - min_x
    height = max_y - min_y

    # Create a transparent surface
    surf = pygame.Surface((width+2, height+2), pygame.SRCALPHA)
    # Draw polygon (shifted to surface coordinates)
    shifted = [(v.x - min_x + 1, v.y - min_y + 1) for v in verts_pg]
    pygame.draw.polygon(surf, color, shifted, 2)

    # Create renderable
    img_service = ImageService()
    img_service.set_image(surf)
    # Set world_pos to the center of the polygon
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    img_service.world_pos = Vector2(center_x, center_y)
    img_service.frect = surf.get_frect(center=(center_x, center_y))

    return img_service
        

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

        caching = True
        try:
            with open(os.path.join(assets_dir, 'settings.json'),'r') as settings:
                print(settings)
                caching = json.load(settings)['SPRITESTACK_OPTIMIZATION']
        except Exception as error:
            print(error)
            caching = True

        self.player_sprite = SpriteStackService(caching)
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

        self.player = Player((-20,100), self.space, 1, self.player_sprite.images[0].get_width(),self.player_sprite.images[0].get_height())
        # self.player_debug_img = wall_visualization(self.player, color=(255,0,0,100))
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
            'paved_road' : image_load(assets_dir,'city_tileset', 'paved_road.png'),
            'road_closed_turn_ne' : image_load(assets_dir,'city_tileset', 'road_closed_turn_ne.png'),
            'road_closed_turn_se' : image_load(assets_dir,'city_tileset', 'road_closed_turn_se.png'),
            'road_closed_turn_sw' : image_load(assets_dir,'city_tileset', 'road_closed_turn_sw.png'),
            'road_closed_turn_nw' : image_load(assets_dir,'city_tileset', 'road_closed_turn_nw.png'),
            'road_straight_thick_left' : image_load(assets_dir,'city_tileset', 'road_straight_thick_left.png'),
            'road_straight_thick_right' : image_load(assets_dir,'city_tileset', 'road_straight_thick_right.png'),
            'road_turn_thick_ne' : image_load(assets_dir,'city_tileset', 'road_turn_thick_ne.png'),
            'road_turn_thick_se' : image_load(assets_dir,'city_tileset', 'road_turn_thick_se.png'),
            'road_turn_thick_sw' : image_load(assets_dir,'city_tileset', 'road_turn_thick_sw.png'),
            'road_turn_thick_nw' : image_load(assets_dir,'city_tileset', 'road_turn_thick_nw.png'),
        }, 35, 35)


        RU = 'road_straight_up'
        RD = 'road_straight_down'
        RR = 'road_straight_right'
        RL = 'road_straight_left'
        NE = 'road_turn_ne'
        SE = 'road_turn_se'
        SW = 'road_turn_sw'
        NW = 'road_turn_nw'

        R1 = 'road_straight_thick_left'
        R2 = 'road_straight_thick_right'
        T1 = 'road_turn_thick_ne'
        T2 = 'road_turn_thick_se'
        T3 = 'road_turn_thick_sw'
        T4 = 'road_turn_thick_nw'

        PO = 'pavement'
        RO = 'road'
        PR = 'paved_road'
        C1 = 'road_closed_turn_ne'
        C2 = 'road_closed_turn_se'
        C3 = 'road_closed_turn_sw'
        C4 = 'road_closed_turn_nw'


        tilemap = [
            [C2,C3,PO,PO,PO,PO,C2,RU,RU,RU,RU,RU,C3,PO,PO,PO,PO,PO,PO],
            [RL,NE,RU,RU,RU,RU,NW,SE,RD,RD,RD,SW,RR,PO,PO,PO,PO,C2,C3],
            [RL,SE,RD,RD,RD,RD,SW,RR,PO,PO,PO,RL,RR,PO,PO,PO,PO,RL,RR],
            [RL,RR,PO,PO,PO,PO,RL,RR,PO,PO,PO,RL,NE,RU,RU,C3,PO,RL,RR],
            [RL,RR,PO,PO,PO,PO,RL,RR,PO,PO,PO,RL,SE,RD,SW,RR,PO,RL,RR],
            [RL,RR,PO,PO,PO,C2,NW,NE,RU,RU,RU,NW,RR,PO,RL,NE,RU,NW,RR],
            [RL,NE,RU,RU,RU,NW,SE,RD,SW,SE,RD,RD,C4,PO,C1,RD,RD,SW,RR],
            [RL,SE,RD,RD,RD,RD,C4,PO,RL,RR,PO,PO,PO,PO,PO,PO,PO,RL,RR],
            [RL,RR,PO,PO,PO,PO,PO,C2,NW,NE,C3,PO,PO,PO,PO,PO,PO,RL,RR],
            [RL,RR,PO,PO,PO,PO,PO,RL,T2,T3,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [RL,NE,C3,PO,PO,PO,PO,RL,R2,R1,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [RL,RO,NE,RU,RU,RU,RU,NW,T1,T4,NE,RU,RU,RU,RU,RU,RU,NW,RR],
            [RL,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RO,RR],
            [C1,RD,RD,RD,RD,RD,RD,SW,SE,SW,SE,RD,RD,RD,RD,RD,RD,SW,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [PO,PO,PO,PO,PO,PO,PO,RL,RR,RL,RR,PO,PO,PO,PO,PO,PO,RL,RR],
            [C2,RU,RU,RU,RU,RU,RU,NW,NE,NW,NE,RU,RU,RU,RU,RU,RU,NW,RR],
            [C1,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,RD,C4],            
            [PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO,PO],            
        ]


        ht = 35/2
        dc = 4 # distance from curb y px
        dc2 = 19-4
        
        self.tile_hitboxes = {
            'road_straight_up' : rect_to_vertices(pygame.FRect(-ht, ht-dc, ht*2, dc)), # done
            'road_straight_down' : rect_to_vertices(pygame.FRect(-ht, -ht, ht*2, dc)), # done
            'road_straight_right' : rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, ht*2)), # done
            'road_straight_left' : rect_to_vertices(pygame.FRect(-ht, -ht, dc, ht*2)), # done
            'road_turn_ne' : rect_to_vertices(pygame.FRect(ht-dc, ht-dc, dc, dc)), # done
            'road_turn_se' : rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, dc)), # done
            'road_turn_sw' : rect_to_vertices(pygame.FRect(-ht, -ht, dc, dc)), # done
            'road_turn_nw' : rect_to_vertices(pygame.FRect(-ht, ht-dc, dc, dc)), # done
            'pavement' : rect_to_vertices(pygame.FRect(-ht, -ht, ht*2, ht*2)), # done
            'road_closed_turn_ne' : [rect_to_vertices(pygame.FRect(-ht, -ht, dc, ht*2)),
                                     rect_to_vertices(pygame.FRect(-ht +dc, -ht, ht*2-dc, dc))], # done

            'road_closed_turn_se' : [rect_to_vertices(pygame.FRect(-ht, -ht, dc, ht*2)),
                                     rect_to_vertices(pygame.FRect(-ht +dc, ht-dc, ht*2-dc, dc))], # done

            'road_closed_turn_sw' : [rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, ht*2)),
                                     rect_to_vertices(pygame.FRect(-ht, ht-dc, ht*2-dc, dc))], # done

            'road_closed_turn_nw' : [rect_to_vertices(pygame.FRect(ht-dc, -ht, dc, ht*2)),
                                     rect_to_vertices(pygame.FRect(-ht, -ht, ht*2-dc, dc))], # done
        
            'road_straight_thick_left' : rect_to_vertices(pygame.FRect(-ht, -ht, dc2, ht*2)),
            'road_straight_thick_right' : rect_to_vertices(pygame.FRect(ht-dc2, -ht, dc2, ht*2)),
            'road_turn_thick_ne' : rect_to_vertices(pygame.FRect(ht-dc2, ht-dc2, dc2, dc2)),
            'road_turn_thick_se' : rect_to_vertices(pygame.FRect(ht-dc2, -ht, dc2, dc2)),
            'road_turn_thick_sw' : rect_to_vertices(pygame.FRect(-ht, -ht, dc2, dc2)),
            'road_turn_thick_nw' : rect_to_vertices(pygame.FRect(-ht, ht-dc2, dc2, dc2))
        }

        no_hitbox = [
            'road', 
            'paved_road',    
        ]

        multiple_hitboxes = [
            'road_closed_turn_sw',
            'road_closed_turn_ne', 
            'road_closed_turn_se',
            'road_closed_turn_nw'
        ]

        self.walls = []
        self.wall_imgs = []
        for y, y_tiles in enumerate(tilemap):
            for x, tile_name in enumerate(y_tiles):
                if tile_name in no_hitbox:
                    continue
                if tile_name in multiple_hitboxes:
                    # Create two walls for the closed turn
                    for i in range(len(self.tile_hitboxes[tile_name])):
                        wall = Wall((x*35 - (len(tilemap[0])*35)/2 +35/2, -y*35 + len(tilemap)*35/2 - 35/2), self.tile_hitboxes[tile_name][i], self.space, 1)
                        self.walls.append(wall)
                        img = wall_visualization(wall)
                        self.wall_imgs.append(img)
                else:
                    # Wall((x*35+35/2+1,-y*35+129), self.tile_hitboxes[tile_name],self.space, 1)
                    wall = Wall((x*35 - (len(tilemap[0])*35)/2 +35/2 , -y*35 + len(tilemap)*35/2 - 35/2), self.tile_hitboxes[tile_name], self.space, 1)
                    self.walls.append(wall)
                    img = wall_visualization(wall)
                    self.wall_imgs.append(img)
                

        tile_size = 35/2

        self.free_roam_tilemap = Map()
        self.free_roam_tilemap.load_tilemap(tilemap)
        self.free_roam_tilemap.load_tileset(self.city_streets_tileset)
        self.free_roam_tilemap.pre_render()
        self.free_roam_tilemap.center = (0,0)

        RO = "ROTONTA"
        LE = "LEFKOS"
        BU = "building"
        KA = "KAMARA"
        LL = "none"

        sprite_stack_tilemap = [
            [LL,LL,LL,LL,BU,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,BU],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,BU,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,BU,BU,LL,LL,LL,LL],
            [LL,LL,LL,BU,LL,BU,LL,LL,LL,RO,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,BU,LL,LL,BU,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,BU,LL,LL],
            [LL,LL,BU,LL,BU,LL,LL,LL,LL,LL,LL,LL,LL,BU,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,BU,LL,LL,BU,LL,BU,LL,LL,LL,BU,LL,LL],
            [LL,LL,BU,BU,LL,LL,BU,LL,LL,LL,LL,BU,LL,LL,BU,LL,LL,LL,LL],
            [LL,LL,LL,BU,LL,LL,BU,LL,LL,LL,LL,LL,BU,LL,LL,LL,BU,LL,LL],
            [LL,LL,LL,LL,BU,LL,BU,LL,LL,LL,LL,LL,LL,BU,BU,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,BU,LL,LL,LL,LL,LL,LL,BU,LL,BU,LL,BU,LL,LL,LL],
            [LL,LL,BU,LL,LL,LL,BU,LL,LL,LL,LL,BU,LL,LL,LL,BU,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,BU,LL,LL,LL,LL,BU,LL,LL,LL,LL,BU,LL,LL],
            [LL,BU,LL,LL,LL,LL,BU,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,BU,LL,BU,LL,LL,LL,LL,BU,LL,BU,LL,LL,BU,LL,LL],
            [LL,BU,LL,LL,LL,BU,LL,LL,LL,LL,LL,BU,LL,LL,LL,BU,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL],            
            [LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LL,LE,LL,LL,LL,LL],            
        ]


        self.rotonta = SpriteStackService(caching)
        self.rotonta.load_images(os.path.join(assets_dir,'ROTONTA'))

        self.lefkos_pirgos = SpriteStackService(caching)
        self.lefkos_pirgos.load_images(os.path.join(assets_dir,'LEFKOS'))

        self.kamara = SpriteStackService(caching)
        self.kamara.load_images(os.path.join(assets_dir,'KAMARA'))

        self.polikatikia = SpriteStackService(caching)
        self.polikatikia.load_images(os.path.join(assets_dir,'building'))

        self.sprite_stack_types = {
            RO: self.rotonta,
            LE: self.lefkos_pirgos,
            BU: self.polikatikia,  # You can load images for buildings as needed
            KA: self.kamara,  # For KAMARA, if you have images
        }

        self.sprite_stacks = []

        for y, y_tiles in enumerate(tilemap):
            for x, tile_name in enumerate(y_tiles):
                ...
        for row_idx, row in enumerate(sprite_stack_tilemap):
            for col_idx, cell in enumerate(row):
                if cell != LL:
                    if cell == RO:
                        stack = self.rotonta
                    elif cell == LE:
                        stack = self.lefkos_pirgos
                    elif cell == BU:
                        stack = SpriteStackService(caching)
                        stack.load_images(os.path.join(assets_dir,'building'))
                    elif cell == KA:
                        stack = self.kamara
                    TILE_SIZE = stack.tile_size  # or whatever your grid size is
                    center_x = col_idx*35 - (len(tilemap[0])*35)/2 +35/2
                    center_y = -row_idx*35 + len(tilemap)*35/2 - 35/2
                    stack.update({'x': center_x, 'y': center_y})
                    self.sprite_stacks.append(stack)

        self.kamara.update({'x': -16, 'y': 35})
        self.sprite_stacks.append(self.kamara)


        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # self.space = pymunk.Space()
        self.temp_angle = 0.0

    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            self.camera_run_setup = False
            SceneManagerMethods.change_current_scene('Menu')

        for event in EngineProperties._events:
            self.player.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    print(f"Display coords: {mouse_x}, {mouse_y}")

                    # Convert display (screen) to world coordinates
                    # 1. Convert to Vector2
                    screen_vec = Vector2(mouse_x, mouse_y)
                    # 2. Undo pymunk_to_pygame (flip y)
                    world_screen = Vector2(screen_vec.x, RendererProperties._display.get_height() - screen_vec.y)
                    # 3. Undo camera transform
                    camera = self.camera
                    rel = world_screen - camera.center_screen
                    rel = rel.rotate_rad(-camera.angle)
                    world_pos = rel + camera.center
                    print(f"World pos: {world_pos.x:.2f}, {world_pos.y:.2f}")

        if keys_pressed[pygame.K_LEFT]:
            self.temp_angle += 0.05
        if keys_pressed[pygame.K_RIGHT]:
            self.temp_angle -= 0.05
        

    def update(self) -> None:
        if not self.camera_run_setup:
            self.camera.update_center_screen((RendererProperties._display.get_width()/2, RendererProperties._display.get_height()/2))
            self.camera_run_setup = True
        
        dt = EngineProperties._dt

        self.space.step(dt)

        self.player.update(dt)

        pos = convert_to_vector2(self.player.body.position)
        self.player_sprite.update_new(
            x = pos.x,
            y = pos.y,
        )
        # When rewriting, this can be optimized
        self.camera.update_center((pos.x,pos.y))
        # self.player_sprite.update_new(
        #     x = int(self.camera.offset_pos.x + RendererProperties._display.get_width()//2),
        #     y = int(self.camera.offset_pos.y + RendererProperties._display.get_height()//2),
        # )
        if GlobalSettings._debug and DebugTags.has_tags(["FPS"]):
            EngineMethods.set_caption(f"{EngineProperties._clock.get_fps():.2f}")

        target_angle = -self.player.body.angle  # or whatever your car's angle is
        lerp_speed = 0.06  # 0 < lerp_speed <= 1, smaller is slower

        # Smoothly interpolate self.angle towards target_angle
        self.angle = lerp_angle(self.angle, target_angle, lerp_speed)
        if GlobalSettings._debug and DebugTags.has_tags(["HITBOXES"]):
            for wall_img in self.wall_imgs:
                # RendererProperties.render_calls.append(wall_renderable)
                wall_img.update()

    

    def render(self) -> None:
        RendererMethods.fill_display(color=(132,126,135))
        self.camera.angle = self.angle

        # Center of rotation is the player's position
        player_pos = convert_to_vector2(self.player.body.position)

        # Render the tilemap with rotation around the player
        self.free_roam_tilemap.render_angle(
            convert_rad_to_deg(self.angle)
        )


        for stack in self.sprite_stacks:
            stack.render(self.angle, bysort=True)

        # Render the player sprite at the center of the screen, only with its own angle
        self.player_sprite.rotation = convert_rad_to_deg(self.player.body.angle + self.angle)
        self.player_sprite.render(bysort=True)

        if GlobalSettings._debug and DebugTags.has_tags(["HITBOXES"]):
            for wall_img in self.wall_imgs:
                # RendererProperties.render_calls.append(wall_renderable)
                wall_img.render_angle(
                    convert_rad_to_deg(self.angle)
                )
            # self.player_debug_img.render_angle(convert_rad_to_deg(self.angle))

        # print(f"Player world position: {player_pos}")

        # # Draw direction line
        # velocity = Vector2(0,-1).rotate_rad(-self.player.body.rotation_vector.angle)
        # if velocity.length() > 0:
        #     velocity_dir = velocity.normalize() * 50  # Length of the line
        #     start_screen = Vector2(RendererProperties._display.get_width() // 2, RendererProperties._display.get_height() // 2)
        #     end_screen = start_screen + velocity_dir
        #     pygame.draw.line(RendererProperties._display, (255, 0, 0), start_screen, end_screen, 3)
