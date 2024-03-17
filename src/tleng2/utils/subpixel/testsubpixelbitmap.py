NUM_BALLS = 500

import pygame
from pygame.locals import *

from subpixelsurface import *

from math import sin, cos

from os import path

dirr = path.join("src","tleng2",'_utils','subpixel','')

def run():
    
    pygame.init()
    screen = pygame.display.set_mode((640, 480))  

    clock = pygame.time.Clock()
    
    pingball = pygame.image.load(dirr + "ball.png")    
    pingball_subpixel = SubPixelSurface(pingball, x_level=4)    
    back = pygame.image.load(dirr + "back.png")
        
    t = 0.
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            if event.type == KEYDOWN:
                return None
        
        time_passed = clock.tick(144)
        t += time_passed / 4000.

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

if __name__ == "__main__":
    run()