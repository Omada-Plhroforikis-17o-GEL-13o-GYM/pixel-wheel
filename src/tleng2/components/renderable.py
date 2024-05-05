from ..engine.properties import RendererProperties
from ..utils.annotations import Color
import pygame

class Renderable:
    def __init__(self,) -> None:
        self.x = 0
        self.y = 0
        self.surface = None # pygame.Surface()
        self.render_method = None


    def __repr__(self):
        return f'x: {self.x}, y: {self.y}, surface: {self.surface}'
    

    @staticmethod
    def rect(rect: pygame.FRect, color: Color, thickness: int, radius: int) -> pygame.SurfaceType:
        """
        To get only the rect, use this method but with the thickness set at 0.
        """   
        surface = None
        if thickness > 0:
            surface = pygame.Surface((rect.w + (thickness<<1),rect.w + (thickness<<1)))
            rect = pygame.Rect(rect.x - thickness, rect.y - thickness, rect.width + thickness*2 , rect.height + thickness*2)
        else:
            surface = pygame.Surface(rect.size)

        temp_rect = rect.copy()
        temp_rect.center = surface.get_frect().center

        pygame.draw.rect(surface, color, temp_rect, abs(thickness), radius)
        return surface
    

    @staticmethod
    def sprite_stack(images, rotation, spread) -> pygame.SurfaceType: ...


    def update_cords(self, 
            x: float,
            y: float
        )-> None: 
        self.x = x
        self.y = y


    def update_cords_rect(self, 
            rect: pygame.FRect
        )-> None: 
        """
        Update the coordinates with a rectangle
        """
        self.x = rect.x
        self.y = rect.y


    def update_surf(self, 
            new_surface: pygame.SurfaceType
        ) -> None: 
        self.surface = new_surface


    def update(self,
            x: float,
            y: float,
            new_surface: pygame.SurfaceType
        ) -> None: 
        self.update_cords(x,y)
        self.update_surf(new_surface)
    

    def render(self,) -> None:
        RendererProperties.render_calls += [self]


    def rendering_method(self, render_method, game_object):
        """
        Gets invoked if the the game object is in the camera area. Used if it has a complex system for rendering 
        e.x. SpriteStacking

        :param render_method: must be a class method, or a function
        """
        self.render_method = render_method
        self.self_class = game_object
        