'''
Offsets the objects so the objects and their hitboxes would show right in the currently displayed game, and for easier debugging
'''
from ..utils import GlobalSettings, GlobalProperties
import pygame

#test
from ..utils.subpixel import SubPixelSurface


class Camera: 
    '''
    Handles how the Surfaces are rendered to the screen. While keeping the world positions.
    '''
    def __init__(self) -> None:
        self.directions = pygame.math.Vector2(0,0)
        self.offset_pos = pygame.math.Vector2(0,0)
        self.rect = pygame.FRect(0,0,GlobalSettings._disp_res[0],GlobalSettings._disp_res[1])
        self.display = GlobalProperties._display 
        # if you want to have multiple cameras. You might also want for them to render in different displays, which then get rendered to the window

    
    def update(self) -> None: ...


    def set_target(self) -> None: ...


    def render(self,
            object: pygame.Surface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area = None,
            special_flags: int = 0 
        ) -> None:

        self.rect.x, self.rect.y = self.offset_pos[0], self.offset_pos[1]

        # GlobalSettings._display.blit(object,
        #                              (game_pos[0]-self.offset_pos[0], 
        #                               game_pos[1]-self.offset_pos[1]),
        #                               area,
        #                               special_flags=special_flags
        #                             )
        GlobalProperties._display.blit(object,
                                     (game_pos[0], 
                                      game_pos[1]),
                                      self.rect,
                                      special_flags=special_flags
                                    )
        # self.draw_rect((255,0,0),self.rect,5) # debug

    def render_exp(self,
            object: SubPixelSurface,
            game_pos: pygame.math.Vector2 | tuple[float,float], 
            area = None,
            special_flags: int = 0 
        ) -> None:

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
                        border_bottom_right_radius
                        )

class Camera_sprite_stacking: 
    def __init__(self) -> None: ...

class Camera_3d: 
    def __init__(self) -> None: ...