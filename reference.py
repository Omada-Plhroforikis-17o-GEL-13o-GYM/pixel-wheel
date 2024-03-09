import sys
import math
import os

import pygame as pg
import pymunk as pm
from pymunk import Vec2d

from pygame.locals import *
flags = DOUBLEBUF


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Player(pg.sprite.Sprite):

    def __init__(self, pos, space, mass=0.3, width=52, height=72):
        super().__init__()
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        #pg.draw.polygon(self.image, pg.Color('steelblue2'),
        #                [(1, 72), (26, 1), (51, 72)])
        pg.draw.polygon(self.image, pg.Color('steelblue2'),
                        [(1, height), (1,1),(width,1) ,(width, height)])
        self.rect = self.image.get_rect(center=pos)
        self.orig_image = self.image
        # The verts for the Pymunk shape in relation
        # to the sprite's center.
        # vertices = [(0, 36), (26, -36), (-26, -36)]
        # vertices = [(-26, 36),(26,36), (26, -36), (-26, -36)]
        vertices = [(-width/2, height/2),(width/2,height/2), (width/2, -height/2), (-width/2, -height/2)]

        # Create the physics body and shape of this object.
        moment = pm.moment_for_poly(mass, vertices)
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vertices, radius=3)
        self.shape.friction = .1
        self.shape.elasticity = .2
        self.body.position = pos
        # Add them to the Pymunk space.
        self.space = space
        self.space.add(self.body, self.shape)

        self.accel_forw = False
        self.accel_back = False
        self.turn_left = False
        self.turn_right = False
        self.topspeed = 1790
        self.angle = 0

    def handle_event(self, event):
        # print(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.accel_forw = True
            if event.key == pg.K_a:
                self.turn_left = True
            if event.key == pg.K_d:
                self.turn_right = True
            if event.key == pg.K_s:
                self.accel_back = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.accel_forw = False
            if event.key == pg.K_a:
                self.turn_left = False
            if event.key == pg.K_d:
                self.turn_right = False
            if event.key == pg.K_s:
                self.accel_back = False

    def update(self, dt):
        # Accelerate the pymunk body of this sprite.
        if self.accel_forw and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, 1624/2), Vec2d(0, 0))
        if self.accel_back and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, -514), Vec2d(0, 0))
        if self.turn_left and self.body.velocity.length < self.topspeed:
            self.body.angle += .1
            self.body.angular_velocity = 0
        if self.turn_right and self.body.velocity.length < self.topspeed:
            self.body.angle -= .1
            self.body.angular_velocity = 0
        # Rotate the image of the sprite.
        self.angle = self.body.angle
        self.rect.center = flipy(self.body.position)
        self.image = pg.transform.rotozoom(
            self.orig_image, math.degrees(self.body.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def __del__(self,):
        self.space.remove(self.body, self.shape)


class Wall(pg.sprite.Sprite):

    def __init__(self, pos, verts, space, mass, *sprite_groups):
        super().__init__(*sprite_groups)
        # Determine the width and height of the surface.
        width = max(v[0] for v in verts)
        height = max(v[1] for v in verts)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(self.image, pg.Color('sienna1'), verts)
        self.rect = self.image.get_rect(topleft=pos)

        moment = pm.moment_for_poly(mass, verts)
        self.body = pm.Body(mass, moment, pm.Body.STATIC)
        # Need to transform the vertices for the pymunk poly shape,
        # so that they fit to the image vertices.
        verts2 = [(x, -y) for x, y in verts]
        self.shape = pm.Poly(self.body, verts2, radius=2)
        self.shape.friction = .9
        self.shape.elasticity = .52
        self.body.position = flipy(pos)
        self.space = space
        self.space.add(self.body, self.shape)

dir = "assets/formula2/"
images = None

def load_images():
    list_dir = os.listdir(dir)
    list_dir.sort()
    images = [pg.image.load(dir + img) for img in list_dir]
    print(images[0].get_width(), images[0].get_height())
    temp_images = []
    for i in images:
        temp_images += [i.convert_alpha()]

    images = temp_images

    return images
    

def load_bimages(width, height):
    list_dir = os.listdir(dir)
    list_dir.sort()
    images = [pg.image.load(dir + img) for img in list_dir]
    print(images[0].get_width(), images[0].get_height())
    temp_images = []
    for i in images:
        temp_images += [pg.transform.scale(i.convert_alpha(),(width,height))]

    images = temp_images

    return images


def spritestack(surf, pos, images, rotation, spread=1, fill=False):
    for i, img in enumerate(images):
        rotated_img = pg.transform.rotate(img, rotation)

        if fill:
            for j in range(spread):
                surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 -i*spread -j))
        
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))

def convert_rad_to_deg(rad) -> float:
    return (rad*180)/math.pi

class Game:

    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((800, 600),flags)
        self.pixel = pg.surface.Surface((800/4, 600/4))
        self.pixel2 = pg.surface.Surface((800/2, 600/2))
        self.pixel3 = pg.surface.Surface((800/1.5, 600/1.5))
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color(60, 60, 60)

        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        self.space.damping = .01

        self.all_sprites = pg.sprite.Group()
        self.images = load_images()
        self.mid_images = load_bimages(width=self.images[0].get_width()*2 , height=self.images[0].get_height()*2)
        self.big_images = load_bimages(width=self.images[0].get_width()*4 , height=self.images[0].get_height()*4)
        self.low_images = load_bimages(width=self.images[0].get_width()*1.5,height=self.images[0].get_height()*1.5)
        print(self.low_images[0].get_height()),self.big_images[0].get_height()
        self.player = Player((100, 300), self.space, width=self.images[0].get_width()*4-10, height=self.images[0].get_height()*4-10)
        self.all_sprites.add(self.player)

        self.pixel_r = False
        self.debug = False

        
        # Position-vertices tuples for the walls.
        vertices = [
            ([80, 120], ((0, 0), (100, 0), (70, 100), (0, 100))),
            ([400, 250], ((20, 40), (100, 0), (80, 80), (10, 100))),
            ([200, 450], ((20, 40), (300, 0), (300, 120), (10, 100))),
            ([760, 10], ((0, 0), (30, 0), (30, 420), (0, 400))),
            ]

        for pos, verts in vertices:
            Wall(pos, verts, self.space, 1, self.all_sprites)

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(60) / 1000
            pg.display.set_caption(f"{self.clock.get_fps():.2f} : FPS")
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    self.debug = False if self.debug else True         
                if event.key == pg.K_v:
                    self.pixel_r += 1 if self.pixel_r < 4 else -3      
                    print(self.pixel_r)
                if event.key == pg.K_ESCAPE:
                    self.all_sprites.remove(self.player)
                    del self.player
                    self.player = Player((100, 300), self.space, width=self.images[0].get_width()*4-10, height=self.images[0].get_height()*4-10)
                    self.all_sprites.add(self.player)

            self.player.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)
        self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.pixel.fill((1,0,0))
        self.pixel2.fill((1,0,0))
        self.pixel3.fill((1,0,0))

        self.all_sprites.draw(self.screen)
        # Debug draw - Pymunk shapes are green, pygame rects are blue.
        if self.debug:
            for obj in self.all_sprites:
                shape = obj.shape
                ps = [flipy(pos.rotated(shape.body.angle) + shape.body.position)
                      for pos in shape.get_vertices()]
                ps.append(ps[0])
                pg.draw.rect(self.screen, pg.Color('blue'), obj.rect, 2)
                pg.draw.lines(self.screen, (90, 200, 50), False, ps, 2)

        print(self.pixel2.get_height())
        
        pos = flipy(self.player.body._get_position()) 
        if self.pixel_r == 1:
            # print(self.player.body._get_angle())
            print(self.player.body._get_angle()) if self.debug else None
            spritestack(self.screen, flipy(self.player.body._get_position()), self.big_images, convert_rad_to_deg(self.player.body._get_angle()),spread=4, fill=True)
        elif self.pixel_r == 2:
            self.pixel2.set_colorkey((1,0,0))
            spritestack(self.pixel2, (pos[0]/2, pos[1]/2), self.mid_images, convert_rad_to_deg(self.player.body._get_angle()),spread=2, fill=True)
            self.screen.blit(pg.transform.scale(self.pixel2,(800,600)),(0,0))
        elif self.pixel_r == 3:
            self.pixel3.set_colorkey((1,0,0))
            spritestack(self.pixel3, (pos[0]/1.5, pos[1]/1.5), self.low_images, convert_rad_to_deg(self.player.body._get_angle()),spread=1.5)
            self.screen.blit(pg.transform.scale(self.pixel3,(800,600)),(0,0))            
        else:
            self.pixel.set_colorkey((1,0,0))
            spritestack(self.pixel, (pos[0]/4, pos[1]/4) , self.images, convert_rad_to_deg(self.player.body._get_angle()))
            self.screen.blit(pg.transform.scale(self.pixel,(800,600)),(0,0))
        
        pg.display.flip()



if __name__ == '__main__':
    pg.init()
    pg.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    Game().run()
    pg.quit()
    sys.exit()