# testing the idea of generating a building from a polygon
# this is a simple pygame script that allows you to draw polygons with the mouse
# and generates a sprite stack from the polygon points
# the sprite stack is then rendered on the screen

import pygame
import random

from pygame.math import Vector2

pygame.init()
display = pygame.display.set_mode((800, 600))
screen = pygame.Surface((400,300))
clock = pygame.time.Clock()

buildings = []
drawing = False
current_poly = []

font = pygame.font.SysFont(None, 28)

def generate_spritestack_polygon(points, layers: int = 50) -> list[pygame.Surface]:
    if len(points) < 3:
        return None, 0, 0, 0
    
    # creating the base image
    min_x = min(pt[0] for pt in points)
    min_y = min(pt[1] for pt in points)

    max_x = max(pt[0] for pt in points)
    max_y = max(pt[1] for pt in points)

    width = max_x - min_x
    height = max_y - min_y

    image = pygame.Surface((width, height), pygame.SRCALPHA)
    # for the point sequence there is a translation to the origin found above.
    pygame.draw.polygon(image, (100, 100, 200), [(pt[0] - min_x, pt[1] - min_y) for pt in points])

    # finding if the polygon has been made in cw or ccw, with the showlace method
    n = len(points)
    s = 0
    for i in range(n-1):
        s += points[i][0]*points[i+1][1] - points[i+1][0]*points[i][1] 
    a = 1/2 * s

    cw = False if a > 0 else True

    vectors = []
    for i in range(len(points)):
        ...

    images = [image]

    for i in range(1,layers):
        temp_image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(temp_image, (0+i*3, 0+i*3, 0+i*3), [(pt[0] - min_x, pt[1] - min_y) for pt in points])
        images += [temp_image]
        
    images[::-1]
    return images

    
running = True
txt = font.render("Left-click to plot building base, right-click to finish", True, (220,220,220))
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Start drawing a new polygon
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click: add point
                current_poly.append((event.pos[0]/2, event.pos[1]/2))  # Scale down for the smaller surface
                drawing = True
            elif event.button == 3 and len(current_poly) >= 3:  # Right click: finish polygon
                # Generate building from polygon
                spritestack = generate_spritestack_polygon(current_poly)
                buildings.append((spritestack, (200, 150)))
                current_poly = []
                drawing = False

    angle += 3
    screen.fill((40, 40, 60))
    # print(buildings)
    for building in buildings:
        if building:
            # Draw the building (spritestack)
            first_rect = building[0][0].get_frect()
            first_rect.center = building[1]
            for y, img in enumerate(building[0]):
                temp = pygame.transform.rotate(img, angle)
                center = temp.get_rect(center=first_rect.center)
                screen.blit(temp, (center[0], center[1]-y-3))

    if drawing and len(current_poly) > 1:
        pygame.draw.lines(screen, (255, 255, 0), False, current_poly, 2)
        for pt in current_poly:
            pygame.draw.circle(screen, (255, 255, 0), pt, 4)

    # Instructions
    screen.blit(pygame.transform.scale(txt, (txt.size[0]/2, txt.size[1]/2)), (20, 20))
    display.blit(pygame.transform.scale(screen, (800,600)), (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()