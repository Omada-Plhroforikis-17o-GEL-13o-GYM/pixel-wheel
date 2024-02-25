import math

import pygame
from pygame import gfxdraw

class Arrow:
    def __init__(self,  
                 start: pygame.Vector2 , 
                 end: pygame.Vector2,
                 color: pygame.Color,
                 body_width: int = 2,
                 head_width: int = 4,
                 head_height: int = 2
                ):
        """
        Draw an arrow between start and end with the arrow head at the end. (No Antialiasing)
    
        Args:
            surface (pygame.Surface): The surface to draw on
            start (pygame.Vector2): Start position
            end (pygame.Vector2): End position
            color (pygame.Color): Color of the arrow
            body_width (int, optional): Defaults to 2.
            head_width (int, optional): Defaults to 4.
            head_height (float, optional): Defaults to 2.
        """
        self.color = color
        self.start = start
        self.end = end
        self.arrow = end - start

        temp_head_height = head_height / 2
        temp_head_width = head_width / 2
        temp_arrow_length = self.arrow.lenth()
        body_length = temp_arrow_length - head_height

        head_verts = [
            pygame.Vector2(0, temp_head_height),  # Center
            pygame.Vector2(temp_head_width, -temp_head_height),  # Bottomright
            pygame.Vector2(-temp_head_width, -temp_head_height),  # Bottomleft
        ]

        if temp_arrow_length >= head_height:
            # Calculate the body rect, rotate and translate into place
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]


    def update(self):
        pass


    def render(self, surface: pygame.Surface, aalias: bool = False):
        pass