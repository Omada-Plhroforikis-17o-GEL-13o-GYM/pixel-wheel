from ..components.renderable import Renderable
from ..engine.properties import RendererProperties
from ..utils.colors import COLOR_KEY, RED
import os
import pygame

class SpriteStackService:
    def __init__(self, caching: bool = False) -> None:
        """
        Rotation is calculated with radians.
        """
        self.renderable = Renderable()
        self.images = None
        self.rotation = 0 # degrees TODO change this to radians

        self.fill = False
        self.spread = 1
        self.rect = None

        self.first_layer_rect = None

        self.caching = caching
        if caching:
            self.cache()        

    def cache(self) -> None: ...


    def load_images(self, directory: str, sprite_set: bool = False) -> None:
        """
        Images in sprite stacking must be consistent, even if in a sprite-set.
        Use os.path.join() for directory parameter.
        """
        list_dir = os.listdir(directory)
        list_dir.sort()
        images = [pygame.image.load(os.path.join(directory, img)) for img in list_dir]
        # print(images[0].get_width(), images[0].get_height())
        temp_images = []
        for i in images:
            temp_images += [i.convert_alpha()]

        self.images: list[pygame.SurfaceType] = temp_images 
        self.rect = self.images[0].get_frect()
        # self.renderable.update
    

    def scale_images(self, scalar) -> None:
        ...


    def render(self,) -> None:
        if self.caching: ... 
        else:
            surf = pygame.Surface(pygame.transform.rotate(self.images[0], self.rotation).get_size())
            sprite_surf = pygame.Surface((surf.get_width(),
                                              surf.get_height() + len(self.images)*self.spread))
            sprite_surf.fill(COLOR_KEY)
            sprite_surf.set_colorkey(COLOR_KEY)

            for i, img in enumerate(self.images):
                rotated_img = pygame.transform.rotate(img, self.rotation)
                if self.fill:
                    for j in range(self.spread):
                        sprite_surf.blit(rotated_img, (0,rotated_img.get_height() // 2 -i*self.spread -j))

                sprite_surf.blit(rotated_img, (0,len(self.images*self.spread) - i*self.spread))
            
            self.renderable.update_surf(sprite_surf)
            self.surf_rect = sprite_surf.get_frect()

            self.surf_rect.bottomleft = self.rect.bottomleft

            pygame.draw.rect(RendererProperties._display,RED,pygame.FRect(self.renderable.x+20,self.renderable.y,sprite_surf.get_width(),sprite_surf.get_height()),3)
            print(self.surf_rect, 'surface_rect')

        self.renderable.update_cords_rect(self.surf_rect)
        self.renderable.render()

        
    def update(self, params: dict = {}) -> None:
        """
        Takes X,Y parameters
        """
        if params != {}:
            self.rect.centerx = params['x']
            self.rect.centery = params['y']
            