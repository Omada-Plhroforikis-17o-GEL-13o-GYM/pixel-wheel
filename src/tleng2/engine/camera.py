'''
Offsets the objects so the objects and their hitboxes would show right in the currently displayed game, easier debugging
'''
from ..utils import GlobalSettings, GlobalProperties
import pygame


class CameraCatcher:
    cameras = {}
    default_camera_key = ''
    default_camera = None

    def __init__(self, camera_key, default_camera):
        if camera_key != None:
            self.cameras.update({camera_key: self})
        else:
            self.cameras.update({f"camera{len(self.cameras)}": self})

        if default_camera and camera_key != None:
            self.default_camera_key = camera_key
            self.default_camera = self
        else:
            self.default_camera_key = f"camera{len(self.cameras)}"
            self.default_camera = self



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
        CameraCatcher.__init__(self,camera_key=camera_name)

        self.width = width
        self.height = height
        self.directions = pygame.math.Vector2(0,0)
        self.offset_pos = pygame.math.Vector2(0,0)
        self.rect = pygame.FRect(0,0,self.width,self.height)
        self.display = GlobalProperties._display 

        self.vertices = [pygame.math.Vector2(-self.width/2, -self.height/2),
                         pygame.math.Vector2(self.width/2 , -self.height/2),
                         pygame.math.Vector2(self.width/2 , self.height/2),
                         pygame.math.Vector2(-self.width/2, self.height/2)]
        self.angle = 0

        # if you want to have multiple cameras. You might also want for them to render in different displays, which then get rendered to the window

    
    def update(self) -> None: ...


    def set_target(self) -> None: ...


    def rotate_v(
            self,
            new_angle
        ) -> None:
        """
        Also rotates the vertices of the camera.
        :param new_angle: Must be in radians
        """
        
        self.angle = new_angle
        temp_vertices = []
        for vertex in self.vertices:
            temp_vertices += [vertex.rotate_rad(new_angle)]


class Camera_3d: 
    def __init__(self) -> None: ...