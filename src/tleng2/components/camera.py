'''
Offsets the objects so the objects and their hitboxes would show right in the currently displayed game, easier debugging
'''
import pygame

from ..engine.settings import GlobalSettings
from ..object.area import VertArea
from ..object.sprite import Sprite



class CameraCatcher:
    cameras = {}
    default_camera_key = ''
    default_camera = None

    def __init__(self, camera_key, default_camera):
        default_key = f"camera{len(self.cameras)}"
        if camera_key != None:
            self.cameras.update({camera_key: self})
        else:
            self.cameras.update({default_key: self})

        if default_camera and camera_key != None:
            self.default_camera_key = camera_key
            self.default_camera = self
        else:
            self.default_camera_key = default_key
            self.default_camera = self

        self.name = camera_key if camera_key != None else default_key
        print(self.cameras)





class Camera(CameraCatcher): 
    '''
    Handles how the Surfaces are rendered to the screen. While keeping the world positions.
    '''
    def __init__(
            self,
            width: int = GlobalSettings._disp_res[0],
            height: int = GlobalSettings._disp_res[1],
            camera_name: str | None = None,
            default_camera: bool = False
        ) -> None:
        """
        self.offset_pos: the coordinates of the camera as a Vector
        self.angle: is measured in radians
        """
        CameraCatcher.__init__(self,camera_key=camera_name, default_camera=default_camera)

        self.vert_area = VertArea(width=width, height=height)

        self.directions = pygame.math.Vector2(0,0)
        
        self.offset_pos = pygame.math.Vector2(0,0)
        self.rect = pygame.FRect(0, 0, self.vert_area.width, self.vert_area.height)

        self.target_entity = None
        


    
    def update(self) -> None: ...


    def set_target(self, new_target_entity: Sprite) -> None: 
        self.target_entity = new_target_entity
        


class Camera_3d: 
    def __init__(self) -> None: ...