from os import path 
import pygame
# from tleng2.utils.annotations import Coordinate
from tleng2.utils.settings import GlobalSettings


class ImageService:
    def __init__(self):
        self.rotation = 0
        self.image = None
        self.image_x = 0
        self.image_y = 0


    def load_image(self,
            img_filename: str,
            width: float,
            height: float,
            ) -> None:
        
        self.image = pygame.image.load(img_filename).convert_alpha() #setting the idle image 
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (width,height)), self.rotation) #transforming the idle image
        self.image_x = self.image.get_width() 
        self.image_y = self.image.get_height()
    

    def render_surface(self)-> pygame.Surface:
        return self.image
    
    
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