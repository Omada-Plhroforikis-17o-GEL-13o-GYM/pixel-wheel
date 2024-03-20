import pygame
from warnings import warn
from ..utils.annotations import Color, VertRect
from ..utils.colors import WHITE, BLACK
from ..engine.settings import GlobalSettings
from ..utils.debug import debug_print
from ..engine.properties import EngineProperties


class AreaCatcher:
    entity_in_scene: dict = {}

    def __init__(self, taint):
        if taint is not False:
            self.entity_in_scene.update({f"area{len(self.camera)}" : [self]})        


class Area(AreaCatcher): # Move area to the entities and stuff
    '''
    Class for area, acts as an area that is dedicated to the entity or the class that inherits this, also can be used for "static" hitboxes.

    Class variables:
        self.rect: the rectangle class from pygame (created for the group sprite object, and as the main hitbox of the Area)
        self.x: the core x coordinate of the rect (it doesn't store the top left coordinate) (float)
        self.y: the core y coordinta of the rect (it doesn't store the top left coordinate) (float)
        self.width: the width of the rectangle (int)
        self.height: the height of the rectangle (int)
        self.image: image (i don't know what it can be used for) (created for the group sprite object) (pygame.Surface)
        self.color: the color of the rectangle (tuple)
    '''
    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            width: float = 10.0,
            height: float = 10.0,
            color: Color = WHITE,
            tainted_area: bool = False
        ) -> None:
        '''
        Initialising the Area
        
        :param x: The Horizontal coordinate (float)
        :param y: The Vertical coordinate (float)
        :param width: The width of the area (float)
        :param height: The height of the area (float)
        :param color: The color of the Area (tuple)
        :param tainted_area: if the area should be catched in the AreaCatcher (bool)
        '''
        super().__init__(tainted_area)
        self.image = pygame.Surface([width,height])
        debug_print(float(x), float(y), float(width) , float(height), type(x), type(y), type(width) , type(height), tags=["EngineAreaInit"])
        self.rect = pygame.FRect(float(x), float(y), float(width) , float(height)) # screen coordinates
        self.x = x # actual x coordinate
        self.y = y # actual y coordinate
        self.width = width
        self.height = height
        self.color = color  

        self.renderer = ...

        self.thickness = 0

    def __repr__(self) -> str:
        if hasattr(self, 'frame_rect') and hasattr(self, 'frame_color'):
            return f"{self.rect} color:{self.color} frame_rect:{self.frame_rect} frame_color:{self.frame_color}"
        else:
            return f"{self.rect} color:{self.color}"


    def collide_area(
            self,
            other_area,
        ) -> bool:
        """
        :param other_area: paramater `other_area` must be of type Class Area.
        :return Area: 
        """
        return self.rect.colliderect(other_area.rect)


    def rectangular_collisions(
            self,
        ) -> tuple:
        """
        :return: Returns from where the collision occured, if no collision occured then it returns (0,0)
        """
        ...


    def render(self) -> None:
        '''
        Draws the area in the screen.
        If there the outline has been set to anything than 0, then it will be rendered
        :return: It returns nothing
        '''
        pygame.draw.rect(EngineProperties._display, self.color, self.rect)
        if self.thickness != 0:            
            pygame.draw.rect(GlobalProperties._display, self.color, self.frame_rect, abs(self.thickness))

    def render_outline(self) -> None:
        '''
        Only renders the outline of the area, the outline needs to be set before it gets rendered.
        :return: It returns nothing
        '''
        pygame.draw.rect(GlobalProperties._display, self.frame_color, self.frame_rect, abs(self.thickness))


    def set_outline(self, 
            thic: float = 1, 
            frame_color: Color = BLACK
        ) -> None:
        '''
        It draws the outline of the area by creating another rect object
        
        :param thic: it's the thickness of the Area's outline, if it is more than 
        :param frame_color: Specifes the color of the area's outline
        :return: it returns nothing
        '''
        self.thickness = thic
        self.frame_color = frame_color
        if thic > 0:
            self.frame_rect = pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2) #outside outline (*performnce issue)
        elif thic <= 0:
            self.frame_color = self.rect
            if thic == 0:
                warn("the thickness of the outline is zero, you can not see it") #giving a "warning" that the thickness of the outline is zero (for performance reasons we could remove it in production)


    def update_entity(
            self,
            x,
            y,
            width,
            height,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height 


    def update(self) -> None:
        '''
        Function for the sprite group updating
        '''

        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

        if self.frame_rect != None:
            self.frame_rect.x = self.x - self.thickness
            self.frame_rect.y = self.y - self.thickness
            # self.frame_rect.width = self.width
            # self.frame_rect.height = self.height
    
    def rounded_update(self) -> None:
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        self.rect.width = round(self.width)
        self.rect.height = round(self.height)

        if self.frame_rect != None:
            self.frame_rect.x = round(self.x - self.thickness)
            self.frame_rect.y = round(self.y - self.thickness)


class LazyArea():
    """
    Fast Area
    """
    ...



class VertArea(Area):
    """
    A Rectangle with vertices.
    The vertices must be 2d not 3d. And there must be 4 vertices not more or less.
    The area is not a polygon, for that you must use PolyArea.
    """
    def __init__(self,
                  x: float = 0, 
                  y: float = 0, 
                  width: float = 10, 
                  height: float = 10
                ) -> None:
        """
        :param vertices: a list of vectors, must be in a list of 4 elements.
        """
        
        Area.__init__(self, x, y, width, height)
        self.vertices = [pygame.math.Vector2(-self.width/2, -self.height/2),
                         pygame.math.Vector2( self.width/2, -self.height/2),
                         pygame.math.Vector2( self.width/2,  self.height/2),
                         pygame.math.Vector2(-self.width/2,  self.height/2)]
        self.angle = 0 # measured in radians

    def rotate_verts(
            self,
            new_angle
        ) -> None:
        """
        Rotates the vertices of the camera.
        rotates around the center
        :param new_angle: Must be in radians
        """
        
        self.angle = new_angle
        temp_vertices = []
        for vertex in self.vertices:
            temp_vertices += [vertex.rotate_rad(new_angle)]
    

    def rotate_point_verts(
            self,
            new_angle,
            point,
        ) -> None:
        """
        Rotates the vertices of the camera.
        rotates around around a given point
        :param new_angle: Must be in radians
        """
        ...

class PolyArea:
    """
    Not implemented yet.
    """
    pass