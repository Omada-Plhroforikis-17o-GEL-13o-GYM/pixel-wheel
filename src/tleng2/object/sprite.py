from .area import Area
from ..services.animation import LazyAnimationService
from ..services.image import ImageService
from ..services.sound import SoundService
from ..engine.settings import GlobalSettings
from ..utils.colors import RED
import pygame


class EntityCatcher:
    entity_in_scene: dict = {}

    def __init__(self, entity_key):
        self.entity_in_scene.update({entity_key:[self]})

# TODO entity has a new meaning now

class Sprite:
    def __init__(
            self,
            x: int | float, 
            y: int | float,  
            width: int | float, 
            height: int | float, 
            sprite_type: str, 
            anim_service_name: str = "LAS"
        ) -> None:

        """
        :param anim_service_name: It's an experimental feature that is designed to hopefully 
                                  make the programmer easily assign anim_services to the entity. 
                                  The default is LAS (LazyAnimationService).
        
                                  - LAS : LazyAnimationService
                                  - IS  : ImageService (static image)
                                  - FAS : FancyAnimationService (not implemented yet)
        
        :return: It returns Nothing (None)
        """
        # these coordinates reference the center of the sprite.
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.FRect(0,0,width,height)
        self.hitbox = Area(x=x, y=y, width=width, height=height)
        #self.set_outline(1,RED)

        self.anim_service_name = anim_service_name
        if anim_service_name == "LAS":
            self.anim_service = LazyAnimationService()
        elif anim_service_name == "IS":
            self.anim_service = ImageService()

        self.anim_service.anim_dict.update({"images":
                                            {"default_surf": pygame.Surface((50,50))}
                                            })
        # self.sound_service = SoundService('')
        self.entity_type = sprite_type

    def load_animation(self, 
            anim_dict: dict
        )-> None:
        try:
            self.anim_service.import_animation(anim_dict=anim_dict)
        except Exception as e:
            raise Exception(f"You tried to load an animation while having the current animation_service: {self.anim_service_name}. \nAdditional Error messages: \n{e}")

    def new_hitbox(self, hitbox_width : float, hitbox_height : float) -> None: # TODO : hitbox/coordination system
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, which is a Rect)
        :param hitbox_width: The new number of the new hitbox width (either a flot or an int)
        :param hitbox_height: The new number of the new hitbox height (either a flot or an int)
        :return: it returns nothing
        '''
        #change the hitbox of the outer box
        self.hitbox.rect.width, self.hitbox.rect.height = hitbox_width, hitbox_height
        self.hitbox.rect.x, self.hitbox.rect.y = self.core_x - self.hitbox.rect.width/2, self.core_y - self.hitbox.rect.height/2


    def update(self) -> None:
        '''
        Updates the logic of sprite.
        '''
        params = {
            "x":self.x,
            "y":self.y,
            "width":self.width,
            "height":self.height
        }
        self.anim_service.update(params)
        self.hitbox.update(params)
    

    def render(self) -> None:
        if GlobalSettings._debug:
            self.hitbox.render_outline()

        self.anim_service.render()


    def update_area(self) -> None:
        """
        Dirty way of updating the area
        """
        self.hitbox.rect.center = (self.x, self.y)
        self.hitbox.width = self.width
        self.hitbox.height = self.height

        # self.hitbox.round_update()
        self.hitbox.update()
    

    #abstraction for this mouthful "koutsoumara" ______________________________________________
    def get_hitbox_x(self) -> float | int:
        return self.hitbox.rect.x
    
    
    def get_hitbox_y(self) -> float | int:
        return self.hitbox.rect.y
    
    
    def get_hitbox_width(self) -> float | int:
        return self.hitbox.rect.width
    
    
    def get_hitbox_height(self) -> float | int:
        return self.hitbox.rect.height
    

    #abstraction for changing the x, y, width, height values    
    def new_hitbox_x(
            self,
            new_x: int | float
        ) -> float | int:
        
        self.hitbox.rect.x = new_x
        self.hitbox.core_x = new_x
    
    
    def new_hitbox_y(
            self,
            new_y: int | float
        ) -> None:
        
        self.hitbox.rect.x = new_y
        self.hitbox.core_x = new_y

    
    
    def new_hitbox_width(
            self,
            new_width: int | float
        ) -> None:
        
        self.hitbox.rect.width = new_width
        self.hitbox.core_width = new_width

        
    def new_hitbox_height(
            self,
            new_height: int | float
        ) -> float | int:
        
        self.hitbox.rect.height = new_height
        self.hitbox.core_height = new_height
    

    def get_hitbox_colliderect(self, *info) -> bool:
        """
        @overload
        def colliderect(self, rect: RectValue, /) -> bool: ...
        @overload
        def colliderect(self, left_top: Coordinate, width_height: Coordinate, /) -> bool: ...
        @overload
        def colliderect(
            self, left: float, top: float, width: float, height: float, /
        ) -> bool: ...
        """
        return self.hitbox.rect.colliderect(*info)
    
    def get_hitbox_collidepoint(
            self, 
            x: float,
            y: float
        ) -> bool:
        """
        x: float
        y: float
        """
        return self.hitbox.rect.collidepoint(x, y)

    # abstraction for changing the hitbox properties
    def new_hitbox_top(
            self,
            new_top: float | int
        )-> None:
        self.hitbox.rect.top = new_top
        self.core_x = self.hitbox.rect.x
        self.core_y = self.hitbox.rect.y


    def new_hitbox_bottom(
            self,
            new_bottom: int
        ) -> None:        
        self.hitbox.rect.bottom = new_bottom
        self.core_y = self.hitbox.rect.y


    def new_hitbox_bottomleft(
            self,
            new_bottomleft:tuple
        ) -> None: 
        self.hitbox.rect.bottomleft = new_bottomleft
        self.core_x = self.hitbox.rect.x
        self.core_y = self.hitbox.rect.y

    
    def new_hitbox_topright(
            self,
            new_topright: tuple
        ) -> None: 
        self.hitbox.rect.topright = new_topright
        self.core_x = self.hitbox.rect.x
        self.core_y = self.hitbox.rect.y


    def new_hitbox_left(
            self,
            new_left: float | int
        )-> None:
        self.hitbox.rect.left = new_left
        self.core_x = self.hitbox.rect.x
        self.core_y = self.hitbox.rect.y

    def new_hitbox_right(
            self,
            new_right: float | int
        )-> None:
        self.hitbox.rect.right = new_right
        self.core_x = self.hitbox.rect.x
        self.core_y = self.hitbox.rect.y

    
    
    
        

