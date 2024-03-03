# import pygame
from ..engine.renderer import Renderer
from ..utils.properties import GlobalProperties

class TileSet:
    def __init__(self, 
            tset,
            width, 
            height
        ) -> None:
        """
        Tile set, 
        {"grass": grass_tile.png,
         "concrete" : concrete_tile.png
         ...}
        """
        
        self.set = tset
        self.width = width
        self.height = height


class TileMap:
    def __init__(self, name):
        self.tiles = []
        self.tileset = {}


    def load_tilemap(self, 
            tilemap: list
        ) -> None:
        """
        Matrix list, if not created in a json file.
        """
        self.tiles = tilemap
    

    def load_tileset(self,
            tileset: TileSet
        ) -> None:
        self.tileset = tileset


    #TODO
    def load_tilemap_json(self,
            tilemap: list
        ) -> None: ...


    def load_tileset_json(self,
            tileset: TileSet
        ) -> None: ...


    def render(self) -> None:
        # Renderer.render_tiles()
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                GlobalProperties._display.blit(self.tileset[self.tiles[y][x]], (x*self.width, y*self.height) )
    

    def update(self) -> None:
        pass