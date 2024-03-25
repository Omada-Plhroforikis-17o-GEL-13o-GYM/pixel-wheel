from ..components.renderable import Renderable
from ..utils.colors import COLOR_KEY
import os
import pygame

class SpriteStackService:
    def __init__(self, caching: bool = False) -> None:
        """
        Rotation is calculated with radians.
        """
        self.renderable = Renderable()
        self.images = None
        self.rotation = 0 # rads

        self.fill = False
        self.spread = 1
        self.rect = None

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
        images = [pygame.image.load(dir + img) for img in list_dir]
        print(images[0].get_width(), images[0].get_height())
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
            surf = pygame.Surface(self.images[0].get_size())
            sprite_surf = pygame.Surface((surf.get_width(),
                                              surf.get_height() + len(self.images)*self.spread))
            sprite_surf.fill(COLOR_KEY)
            sprite_surf.set_colorkey(COLOR_KEY)

            for i, img in enumerate(self.images):
                rotated_img = pygame.transform.rotate(img, self.rotation)
                if self.fill:
                    for j in range(self.spread):
                        sprite_surf.blit(rotated_img, (self.rect.x - rotated_img.get_width() // 2, self.pos[1] - rotated_img.get_height() // 2 -i*self.spread -j))

                sprite_surf.blit(rotated_img, (self.pos[0] - rotated_img.get_width() // 2, self.pos[1] - rotated_img.get_height() // 2 - i * self.spread))
            
            self.renderable.update_surf(sprite_surf)

        self.renderable.render()

        
    def update(self,params: dict = {}) -> None:
        if params is not {}:
            self.rect.center = (params['x'], params['y'])
            self.renderable.update_cords_rect(self.rect)