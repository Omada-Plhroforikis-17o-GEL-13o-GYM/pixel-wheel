from pymunk import Vec2d
from .tleng2 import GlobalSettings

import pygame
import pymunk
import math

def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+GlobalSettings._disp_res[1])

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, space, mass=0.3, width=52, height=72):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        #pygame.draw.polygon(self.image, pygame.Color('steelblue2'),
        #                [(1, 72), (26, 1), (51, 72)])
        pygame.draw.polygon(self.image, pygame.Color('steelblue2'),
                        [(1, height), (1,1),(width,1) ,(width, height)])

        self.rect = self.image.get_rect(center=pos)
        self.orig_image = self.image

        # The verts for the Pymunk shape in relation
        # to the sprite's center.
        # vertices = [(0, 36), (26, -36), (-26, -36)]
        # vertices = [(-26, 36),(26,36), (26, -36), (-26, -36)]

        vertices = [(-width/2, height/2),(width/2,height/2), (width/2, -height/2), (-width/2, -height/2)]

        # Create the physics body and shape of this object.
        moment = pymunk.moment_for_poly(mass, vertices)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vertices, radius=3)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.accel_forw = True
            if event.key == pygame.K_a:
                self.turn_left = True
            if event.key == pygame.K_d:
                self.turn_right = True
            if event.key == pygame.K_s:
                self.accel_back = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.accel_forw = False
            if event.key == pygame.K_a:
                self.turn_left = False
            if event.key == pygame.K_d:
                self.turn_right = False
            if event.key == pygame.K_s:
                self.accel_back = False

    def update(self, dt):
        # Accelerate the pymunk body of this sprite.
        if self.accel_forw and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, 1624/2) , Vec2d(0, 0))
        if self.accel_back and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, -514) , Vec2d(0, 0))
        if self.turn_left and self.body.velocity.length < self.topspeed:
            self.body.angle += .08 * dt * 100
            self.body.angular_velocity = 0
        if self.turn_right and self.body.velocity.length < self.topspeed:
            self.body.angle -= .08 * dt * 100
            self.body.angular_velocity = 0
        # Rotate the image of the sprite.
        self.angle = self.body.angle
        self.rect.center = flipy(self.body.position)
        self.image = pygame.transform.rotozoom(
            self.orig_image, math.degrees(self.body.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def __del__(self,):
        self.space.remove(self.body, self.shape)


class Wall():

    def __init__(self, pos, verts, space, mass):
        # Determine the width and height of the surface.
        # width = max(v[0] for v in verts)
        # height = max(v[1] for v in verts)
        # self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # pygame.draw.polygon(self.image, pygame.Color('sienna1'), verts)
        # self.rect = self.image.get_rect(topleft=pos)

        moment = pymunk.moment_for_poly(mass, verts)
        self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        # Need to transform the vertices for the pymunk poly shape,
        # so that they fit to the image vertices.
        # verts2 = [(x, -y) for x, y in verts]
        self.shape = pymunk.Poly(self.body, verts, radius=2)
        self.shape.friction = .9
        self.shape.elasticity = .52
        self.body.position = pos
        self.space = space
        self.space.add(self.body, self.shape)

    