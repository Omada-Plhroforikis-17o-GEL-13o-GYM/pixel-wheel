# Tilemap used for a map

from ..services.tilemap import TileMap
from ..engine.properties import RendererProperties
from ..components.renderable import Renderable


import pygame

class Map(TileMap):
    '''
    Requires Tiles that have objects in render.
    '''
    def __init__(self) -> None:
        self.renderable = Renderable()


    def pre_render(self) -> None:
        # Renderer.render_tiles()

        surf = pygame.Surface((self.tileset.width*len(self.tiles[0]), self.tileset.height*len(self.tiles)))

        for y, y_tiles in enumerate(self.tiles):
            for x, tile_name in enumerate(y_tiles):
                # print(tile_name,self.tileset.set[tile_name])
                
                surf.blit(self.tileset.set[tile_name],(x*self.tileset.width, y*self.tileset.height))
                # self.renderable.update(x*self.tileset.width, y*self.tileset.height, self.tileset.set[tile_name])
                # self.renderable.render()

        self.renderable.update_surf(surf)


    def render(self) -> None:
        # RendererProperties._display.blit
        self.renderable.render()


    def add_to_space(self, space):
        """
        Adds the physics side of the tiles to space (pymunk)
        """
        for y, y_tiles in enumerate(self.tiles):
            for x, tile_name in enumerate(y_tiles):
                # print(tile_name,self.tileset.set[tile_name])
                space.add() 