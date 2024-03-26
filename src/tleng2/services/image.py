from ..components.renderable import Renderable

import pygame
# from tleng2.utils.annotations import Coordinate
# from ..utils.settings import GlobalSettings


class ImageService:
    def __init__(self):
        self.rotation = 0
        self.image = None
        self.renderable = Renderable()


    def load_image(self,
            img_filename: str,
            width: float,
            height: float,
            ) -> None:
        
        self.image = pygame.image.load(img_filename).convert_alpha() #setting the idle image 
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (width,height)), self.rotation) #transforming the idle image
        self.rect = pygame.FRect(0,0,self.image.get_width(),self.image.get_height())
    

    def render_surface(self)-> pygame.Surface:
        return self.image
    
    def update(self,params: dict = {}):
        if params != {}:
            ...
        else:
            self.renderable.update_cords_rect(self.rect)

    def render(self) -> None:
        self.renderable.update_surf(self.render_surface())
        self.renderable.render()
    
    def rotate_img_deg(self,
            rotate: float
            ) -> None:
        '''
        Rotates the image by some given angle (degrees)
        '''
        pass


    def rotate_img_rad(self,
            rotate: float
            ) -> None:
        '''
        Rotates the image by some given angle (radians)
        '''
        pass


    def flip_img(self,
            flip_x: bool = False,
            flip_y: bool = False,
            ) -> None:
        '''
        Flips an image to the according axis
        '''
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)


    def scale_img_px(self,
            width: float, 
            height: float, 
            ) -> None:
        '''
        Scale the image to the new desired res (uses pixels) 
        '''


    def scale_img_per(self,
            per: float
            ) -> None: 
        '''
        Scale the image to the new desired res (uses percentage) 
        '''


    def scale_img_dpi(self) -> None:
        '''
        TODO
        '''
        raise NotImplementedError('Function "scale img to dpi" has not been implemented')