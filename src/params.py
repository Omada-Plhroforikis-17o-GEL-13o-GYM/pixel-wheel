from .tleng2 import RendererMethods
from .tleng2.components.camera import CameraCatcher


def import_params_needed() -> None:
    RendererMethods.import_scene_renderer_params_dict({
        'free_roam':{
            'display' : RendererMethods.load_local_display_ratio(1/3),
            'camera' : 'camera0'
        } 
    })