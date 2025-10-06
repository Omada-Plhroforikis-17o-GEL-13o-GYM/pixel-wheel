# testing the idea of generating a building from a polygon
# this is a simple pygame script that allows you to draw polygons with the mouse
# and generates a sprite stack from the polygon points
# the sprite stack is then rendered on the screen

import pygame
import random

from math import pi
from pygame.math import Vector2

pygame.init()
display = pygame.display.set_mode((800, 600))
screen = pygame.Surface((400,300))
clock = pygame.time.Clock()

buildings = []
drawing = False
current_poly = []

font = pygame.font.SysFont(None, 28)

def state(i: int, alts: int, layers: int) -> bool:
    total_length = layers
    segment_length = total_length / (alts *2)
    segment_index = int(i // segment_length)
    return segment_index % 2 == 0

def balcony_layer_spans(layers: int, levels: int, base_fraction: float = 0.1) -> list[tuple[int, int, int]]:
    """
    Returns a list of (start_layer, base_end_layer, end_layer, balcony) for each balcony.
    - start_layer: first layer of the balcony span
    - base_end_layer: last layer for the base (first base_fraction of the span)
    - end_layer: last layer of the balcony span (railings go up to here)
    """
    spans = []

    for i in range(levels):
        span_length = layers // levels
        start_layer = i * span_length
        end_layer = (i + 1) * span_length if i < levels - 1 else layers
        base_end_layer = start_layer + int((end_layer - start_layer) * base_fraction)
        if base_end_layer == start_layer:
            base_end_layer += 1
        
        balcony = start_layer + (span_length // 2)

        spans.append((start_layer, base_end_layer, end_layer, balcony))

    return spans


def generate_spritestack_polygon(points: list[tuple], layers: int = 40, bpe: int = 4) -> list[pygame.Surface]:
    """
    bpe: means Balconies Per Edge (side of the polygon).
    """
    if len(points) < 3:
        return None, 0, 0, 0
    
    or_points = points.copy()

    # finding if the polygon has been made in cw or ccw, with the shoelace method
    n = len(points)
    s = 0
    for i in range(n-1):
        s += points[i][0]*points[i+1][1] - points[i+1][0]*points[i][1] 
    a = 1/2 * s

    cw = False if a > 0 else True

    vectors: list[Vector2] = []
    point_vectors: list[Vector2] = []

    # TODO probably a small logic problem with the -1
    for i in range(len(points)):
        vectors.append(Vector2(points[i]) - Vector2(points[i-1])) # AB = B - A
        point_vectors.append(Vector2(points[i-1]))

    balcony_threshold = 50

    balconies: list[list[Vector2]] = []
    railings: list[list[Vector2]] = []
    for i, vector in enumerate(vectors):
        l = vector.length()
        v = vector.normalize()  # Direction along the edge
        scalar = 15

        # Perpendicular direction
        if cw:
            v1 = v.rotate_rad(pi/2) * scalar
        else:
            v1 = v.rotate_rad(-pi/2) * scalar

        start = Vector2(points[i-1])

        possible_balconies = int(l // balcony_threshold)
        edge_bpe = min(bpe, max(1, possible_balconies))

        balcony_width_fraction = 0.9
        side_barrier_fraction = 0.95

        for b in range(edge_bpe):
            # Compute the available fraction for balconies
            available_fraction = 1.0 - 2 * side_barrier_fraction
            # Space balconies evenly within the available fraction
            t0 = side_barrier_fraction + (b + 0.0) * available_fraction / edge_bpe
            t1 = t0 + balcony_width_fraction * available_fraction / edge_bpe
            p0 = start + v * (l * t0)
            p1 = start + v * (l * t1)
            balcony_poly = [
                p0,
                p0 + v1,
                p1 + v1,
                p1
            ]
            balconies.append(balcony_poly)

    all_balcony_points: list[tuple] = []
    for balcony in balconies:
        for v in balcony:
            all_balcony_points.append((v.x, v.y))

    all_points = points + all_balcony_points

    # creating the base image
    min_x = min(pt[0] for pt in all_points)
    min_y = min(pt[1] for pt in all_points)

    max_x = max(pt[0] for pt in all_points)
    max_y = max(pt[1] for pt in all_points)

    width = max_x - min_x
    height = max_y - min_y

    print(width, height)

    points = [(pt[0] - min_x, pt[1] - min_y) for pt in or_points]
    temp_balconies = []
    for balcony in balconies:
        temp_balconies.append([Vector2(v.x - min_x, v.y - min_y) for v in balcony])
    balconies = temp_balconies.copy()

    image = pygame.Surface((round(width), round(height)), pygame.SRCALPHA)

    pygame.draw.polygon(image, (100, 100, 200), points)
    pygame.draw.rect(image, "RED", (0,0,width,height), 1) # DEBUG

    # print(len(points), len(vectors))
    images = [image]
    levels = 5
    spans = balcony_layer_spans(layers, levels)
    print(spans)
    for i in range(layers):
        temp_image = pygame.Surface((width, height), pygame.SRCALPHA)
        # pygame.draw.polygon(temp_image, (0+i*3, 0+i*3, 0+i*3), points)
        current_level = int(i/(layers/levels))
        if i in range(spans[current_level][0], spans[current_level][3]): # if we are in range of the balcony
            if i in range(spans[current_level][0],spans[current_level][1]): # in the range of the base
                for balcony in balconies:
                    pygame.draw.polygon(temp_image, (100-i*2, 100-i*2, 100-i*2), balcony)
                    pygame.draw.polygon(temp_image, "RED", balcony, 1) # DEBUG

            if i in range(spans[current_level][1],spans[current_level][3]-1): # in the range of the railings
                for balcony in balconies:
                    print(len(balcony), balcony)
                    railing_color = (180, 180, 180)
                    p0_outer = balcony[2]
                    p1_outer = balcony[1]
                    l = p0_outer.distance_to(p1_outer)
                    railing_count = int(l/4)  # Number of railings per balcony
                    for r in range(1,railing_count):
                        t = r / railing_count
                        railing_start = p0_outer.lerp(p1_outer, t)
                        railing_end = railing_start - (balcony[1] - balcony[0]) * 0.5  # Halfway down to the inner edge
                        railing_point = railing_start - (balcony[1] - balcony[0]) * 0.2  # Halfway down to the inner edge
                        # pygame.draw.line(temp_image, railing_color, railing_start, railing_end, 2)
                        pygame.draw.circle(temp_image, railing_color, railing_point, 1)

            print(range(spans[current_level][3]-1,spans[current_level][3]), i)

            if i in range(spans[current_level][3]-1,spans[current_level][3]):
                for balcony in balconies:
                    ...
                    # p1 = balcony[0].copy()
                    # p2 = balcony[1].copy()

                    # m = (p2 - p1)*0.5


                    # b = balcony.copy()
                    # pygame.draw.polygon(temp_image, (100,100,100), )
                    
                    # for poing in balcony:
                    # pygame.draw.circle(temp_image, (50*j,50*j,50*j), (point.x, point.y), 2) # DEBUG
                    # print((50*j,50*j,50*j))
                    
                        
        images += [temp_image]
        
    images[::-1]
    return images

    
running = True
txt = font.render("Left-click to plot building base, right-click to finish", True, (220,220,220))
angle = 0
rotate_enabled = True
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
                buildings.append((spritestack, (200, 175)))
                current_poly = []
                drawing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rotate_enabled = not rotate_enabled  # Toggle rotation

    if rotate_enabled:
        angle += 0.7

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
    display.blit(pygame.transform.scale(screen, (800,600)), (0, 0))
    display.blit(pygame.transform.scale(txt, (txt.size[0], txt.size[1])), (20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()