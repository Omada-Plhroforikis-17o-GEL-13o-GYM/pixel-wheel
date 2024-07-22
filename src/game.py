"""
Gameplay scene class
"""
from .tleng2 import *
from .physics import Player, Wall

from pygame import Vector2
from pymunk import Vec2d
import pymunk
import pygame
import os
import json


def flipy(p):
    """Convert chipmunk coordinates to pygame screen coordinates."""
    return Vec2d(p[0], -p[1]+RendererProperties._display.get_size()[1])

def flipy_pymunk(p) -> float:
    """."""
    return Vec2d(p[0], -p[1]+RendererProperties._display.get_size()[1])


def image_load(*path) -> pygame.SurfaceType:
    return pygame.image.load(os.path.join(*path)).convert_alpha()


def rect_to_vertices(rect) -> list[Vector2]:
    return [Vec2d(*rect.topleft), Vec2d(*rect.topright), Vec2d(*rect.bottomright), Vec2d(*rect.bottomleft)]




class FreeRoam(Scene):
    def __init__(self, scene_name) -> None:
        self.camera = Camera(default_camera = True)
        super().__init__(scene_name,'free_roam')
        assets_dir = os.path.join(get_parent_dir(__file__,2), 'assets')

        
        self.debug = True

        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        self.space.damping = .01

        self.player_sprite = SpriteStackService()
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

        print(self.player_sprite.images[0].get_width(),self.player_sprite.images[0].get_height())

        

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
            [RO,RR,PO,RO,PO,RL,NE,RU,RU,RU,NW,RO,RO],
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
                    Wall((x*35+35/2+1,-y*35+129), self.tile_hitboxes[tile_name],self.space, 1)
                

        tile_size = 35/2

        self.free_roam_tilemap = Map()
        self.free_roam_tilemap.load_tilemap(tilemap)
        self.free_roam_tilemap.load_tileset(self.city_streets_tileset)
        self.free_roam_tilemap.pre_render()


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
                     self.polikatikia6]

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # self.space = pymunk.Space()

    def event_handling(self, keys_pressed) -> None:                    
        if keys_pressed[pygame.K_ESCAPE]:
            SceneManagerMethods.change_current_scene('Menu')
        for event in EngineProperties._events:
            self.player.handle_event(event)


    def update(self) -> None:
        self.space.step(EngineProperties._dt)

        self.player.update(EngineProperties._dt)
        pos = flipy(self.player.body._get_position())
        angl = convert_rad_to_deg(self.player.body._get_angle())
        self.camera.offset_pos = Vector2(pos[0],pos[1]) - Vector2(RendererProperties._display.get_width()/2, RendererProperties._display.get_width()/2) 

        self.player_sprite.update(params={
            'x':int(self.camera.offset_pos.x + RendererProperties._display.get_width()//2),
            'y':int(self.camera.offset_pos.y + RendererProperties._display.get_height()//2),
        })

        self.player_sprite.rotation = angl

        # print(angl,self.player.body._get_angle())

        # self.rotonta.update({'x':35,'y':50})
        # self.lefkos_pirgos.update()
    

    def render(self) -> None:
        RendererMethods.fill_display(color=(34,32,52))
        self.free_roam_tilemap.render()

        # if self.debug:
        #     for obj in self.all_sprites:
        #         shape = obj.shape
        #         ps = [flipy(pos.rotated(shape.body.angle) + shape.body.position)
        #               for pos in shape.get_vertices()]
        #         ps.append(ps[0])
        #         pygame.draw.rect(RendererProperties._display, pygame.Color('blue'), obj.rect, 2)
        #         pygame.draw.lines(RendererProperties._display, (90, 200, 50), False, ps, 2)
        # self.player_sprite.spread = 8
        self.player_sprite.render()
        #print(self.player_sprite.rect, 'player rect')
        
        #pygame.draw.rect(RendererProperties._display,(255,0,0),self.player_sprite.rect)

        self.rotonta.render()
        self.lefkos_pirgos.render()

        for building in self.buildings:
            building.render()

        # no_hitbox = ['road', 'paved_road']

        # print('1points____________________________________________________________________')
        # for x, y_tiles in enumerate(self.free_roam_tilemap.tiles):
        #     for y, tile_name in enumerate(y_tiles):
        #         if tile_name in no_hitbox:
        #             continue
        #         else:
        #             temp_points = []
                    
        #             for point in self.tile_hitboxes[tile_name]:
        #                 temp_points += [Vector2(point.x*x*35,point.y*y*35) - self.camera.offset_pos]

        #             print(temp_points)
        #             pygame.draw.lines(RendererProperties._display, (255,0,0), False, temp_points)

        # print('2points ___________________________________________________________________')


        #pygame.draw.circle(RendererProperties._display,(255,0,0), ())

        