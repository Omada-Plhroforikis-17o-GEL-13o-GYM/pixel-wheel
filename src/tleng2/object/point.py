from pygame import Vector2, draw, surface
from ..components.renderable import Renderable
from ..utils.colors import RED
from ..utils.annotations import Color

class Point:
    """
    Point in 2d space.
    A way to store the x,y values.
    Used to declare the center of smt.
    """
    def __init__(self, 
            x: int | float , 
            y: int | float, 
            radius: int = 1,
            color: Color = RED
        ) -> None:
        self.point = Vector2(x,y)
        self.renderable = Renderable()
        self.renderable.update_cords(x,y)
        self.renderable.update_surf(surface.Surface((radius*2,radius*2)))
        draw.circle(self.renderable.surface,color,(radius, radius), radius)

    def update(self, 
            x: int | float, 
            y: int | float
        ) -> None:
        self.point.x = x
        self.point.y = y
        self.renderable.update_cords(x,y)


    def render(self) -> None:
        self.renderable.render()
