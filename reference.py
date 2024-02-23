import sys
import math

import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Player(pg.sprite.Sprite):

    def __init__(self, pos, space, mass=0.3):
        super().__init__()
        self.image = pg.Surface((52, 72), pg.SRCALPHA)
        #pg.draw.polygon(self.image, pg.Color('steelblue2'),
        #                [(1, 72), (26, 1), (51, 72)])
        pg.draw.polygon(self.image, pg.Color('steelblue2'),
                        [(1, 72), (1,1),(51,1) ,(51, 72)])
        self.rect = self.image.get_rect(center=pos)
        self.orig_image = self.image
        # The verts for the Pymunk shape in relation
        # to the sprite's center.
        # vertices = [(0, 36), (26, -36), (-26, -36)]
        vertices = [(-26, 36),(26,36), (26, -36), (-26, -36)]

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
        print(event)
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
            self.body.apply_force_at_local_point(Vec2d(0, 624), Vec2d(0, 0))
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


class Game:

    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color(60, 60, 60)

        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        self.space.damping = .01

        self.all_sprites = pg.sprite.Group()

        self.player = Player((100, 300), self.space)
        self.all_sprites.add(self.player)
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
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            self.player.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)
        self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.all_sprites.draw(self.screen)
        # Debug draw - Pymunk shapes are green, pygame rects are blue.
        for obj in self.all_sprites:
            shape = obj.shape
            ps = [flipy(pos.rotated(shape.body.angle) + shape.body.position)
                  for pos in shape.get_vertices()]
            ps.append(ps[0])
            pg.draw.rect(self.screen, pg.Color('blue'), obj.rect, 2)
            pg.draw.lines(self.screen, (90, 200, 50), False, ps, 2)

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()
    sys.exit()