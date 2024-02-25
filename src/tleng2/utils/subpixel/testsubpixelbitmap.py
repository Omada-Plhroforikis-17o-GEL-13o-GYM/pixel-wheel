NUM_BALLS = 100

import pygame
from pygame.locals import *

from subpixelsurface import *

from math import sin, cos

def run():
    
    pygame.init()
    screen = pygame.display.set_mode((640, 480))  

    clock = pygame.time.Clock()
    
    pingball = pygame.image.load("subpixel/ball.png")    
    pingball_subpixel = SubPixelSurface(pingball, x_level=4)    
    back = pygame.image.load("subpixel/back.png")
        
    t = 0.
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                return
        
        time_passed = clock.tick(144)
        t+= time_passed / 4000.

        screen.blit(back, (0, 0))

        for n in range(NUM_BALLS):
            a = float(n)/NUM_BALLS * 40.
            x = sin((t+a)*.74534) * 100. + 160
            y = cos(((t*1.232)+a)*.453464) * 100. + 240.
                        
            screen.blit(pingball, (x, y))
            # print("non - ", x,y)
            screen.blit(pingball_subpixel.at(x,y), (x+320, y))
            # print("sub - ",x,y)
       
        pygame.display.update() 
        # print(time_passed)

        
run()