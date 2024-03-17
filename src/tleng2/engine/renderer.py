from ..utils.properties import GlobalProperties
from ..utils.properties import GlobalSettings
from ..core_engine.engine import EngineProperties
from ..utils.subpixel import SubPixelSurface
from ..utils.debug import debug_print
from .camera import Camera, CameraCatcher

from abc import ABC
import pygame


class Renderer(ABC):
    def __init__(self) -> None:
        self.layers = []
        self.layers_order = None
        self.target_surf = None # defalut is EngineProperties._display


    def add_layer(
            self,
            width: int | None = None,
            height: int | None = None
        ) -> None:
        """
        Either you input the width and the height, or leave it blank.
        """
        if width == None and height == None:
            self.layers += [pygame.Surface(GlobalSettings._disp_res)]
        else:
            self.layers += [pygame.Surface((width, height))]

    def add_layers(
            self,
            layers: list[pygame.SurfaceType]
        ) -> None:
        """
        Adds multiple layers at once.
        """
        self.layers += layers


    def change_layers_order(self) -> None: ...


    def render_surface(self,
            object: pygame.Surface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area: pygame.Rect = None,
            special_flags: int = 0,
            layer_key: str = None,
            camera: str = None
        ) -> None:

        self.rect.x, self.rect.y = self.offset_pos[0], self.offset_pos[1]
        
        if area != None:
            GlobalSettings._display.blit(object,
                                         (game_pos[0]-self.offset_pos[0], 
                                          game_pos[1]-self.offset_pos[1]),
                                          area,
                                          special_flags=special_flags
                                        )
        else:
            GlobalProperties._display.blit(object,
                                         (game_pos[0], 
                                          game_pos[1]),
                                          self.rect,
                                          special_flags=special_flags
                                        )
        # self.draw_rect((255,0,0),self.rect,5) # debug


    def render_sub_exp(self,
            object: SubPixelSurface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area: pygame.Rect = None,
            special_flags: int = 0 
        ) -> None:
        """
        experimental renderer
        """
        self.rect.x, self.rect.y = self.offset_pos[0], self.offset_pos[1]

        # GlobalSettings._display.blit(object,
        #                              (game_pos[0]-self.offset_pos[0], 
        #                               game_pos[1]-self.offset_pos[1]),
        #                               area,
        #                               special_flags=special_flags
        #                             )
        GlobalProperties._display.blit(object.at(game_pos[0], game_pos[1]),
                                     (game_pos[0], 
                                      game_pos[1]),
                                      self.rect,
                                      special_flags=special_flags
                                    )


    def draw_rect(self,
            color: tuple[int,int,int],
            rect: pygame.Rect,
            width: int,
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1,
        ) -> None:
        '''
        Renders the rectangle into the window, with the camera offset.
        '''
        dummy_rect = rect.copy()
        dummy_rect.x -= int(self.offset_pos[0])
        dummy_rect.y -= int(self.offset_pos[1])
        pygame.draw.rect(GlobalProperties._display, 
                        color,
                        dummy_rect,
                        width,
                        border_radius,
                        border_top_left_radius,
                        border_top_right_radius,
                        border_bottom_left_radius,
                        border_bottom_right_radius)


    def render_tiles(self, layer, camera) -> None:
        """
        It will render every single tile in the level that is provided.
        """
        if self.layers == []:
            ...
        else:
            # usage of layer
            ...

    
    def lazy_render_tiles(self, layer, camera) -> None:
        """
        Will only render where the camera is hovering at from the chunks that are provided (Even if it is rotated).
        """
        # Require the tilemap to be broken up into chunks
