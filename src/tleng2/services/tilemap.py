from ..components.renderable import Renderable
from ..engine.properties import EngineProperties, RendererProperties

from abc import ABC, abstractmethod

from pygame import Vector2
import pygame

class Tile(ABC):
    def __init__(self) -> None:
        '''
        {'name':{
                'render' : [ImageService, SpriteStack]
                'physics' : [Wall]
            }
        }
        '''
        super().__init__()
        self.pos = Vector2()
        self.properties = {}
    

    def update_position() -> None:
        ...

    @abstractmethod
    def update(self) -> None: ...


    @abstractmethod
    def render() -> None:
        ...
        

class TileSet:
    def __init__(self, 
            tset,
            width, 
            height
        ) -> None:
        """
        For images use ImageService
        Tile set, 
        {"grass": GrassTile,
         "concrete" : ConcreteTile,
         ...}
        """
        
        self.set = tset
        self.width = width
        self.height = height

class TileMap:
    def __init__(self):
        self.tiles = []
        self.tileset = {}
        


    def load_tilemap(self, 
            tilemap: list
        ) -> None:
        """
        Matrix list, if not created in a json file.
        """
        self.tiles = tilemap

        # more calculations, for baking in tile coordinates and other.
    

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


    def get_info(self, key) -> None:
        """
        The key to help with the giving back all the info from 
        """


    def update(self) -> None:
        """
        Update Animations and stuff in the tiles.
        """
        pass