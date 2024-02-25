# import pygame

class TileSet:
    def __init__(self, 
            width, 
            height
        ) -> None:
        self.width = width
        self.height = height
    
    def import_set(self, 
        set: dict
        ) -> None:
        self.set = set


class TileMap:
    def __init__(self):
        self.tiles = []
        self.tileset = {}


    def load_tilemap(self, 
            tilemap: list
        ) -> None:
        self.tiles = tilemap
    

    def import_tiles(self,
            tileset: TileSet
        ) -> None:
        self.tileset = tileset


    def render(self) -> None:
        pass
    

    def update(self) -> None:
        pass