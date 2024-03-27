from ..components.scene import SceneCatcher
from .properties import EngineProperties, SceneManagerProperties, RendererProperties
from .settings import GlobalSettings

import pygame

class EngineMethods:
    @staticmethod
    def set_caption(caption: str) -> None:
        pygame.display.set_caption(caption)

    
    @staticmethod
    def clock_tick_dt(target_fps: int) -> float:
        return EngineProperties._clock.tick(target_fps) / 1000
        # return 1
    

    @staticmethod
    def clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) / 1000


    # micro optimization
    @staticmethod
    def lazy_clock_tick_GP_dt(target_fps: int) -> None:
        """
        Stores the dt value in EngineProperties.
        """
        EngineProperties._dt = EngineProperties._clock.tick(target_fps) >> 10 # bit shift, clock.tick / 1024
    


class SceneManagerMethods:
    """
    SceneManager Static methods that might be needed across the base game.
    """
    @staticmethod
    def start_with_scene(scene_name: str) -> None:
        """
        Declares the default scene.
        """
        
        SceneManagerProperties._current_scene = scene_name
        
        params = RendererProperties.type_parameters[RendererProperties.scene_parameters[SceneManagerProperties._current_scene]]
        RendererProperties._display = params['display']
        RendererProperties._local_default_camera = params['camera']
        


    @staticmethod
    def change_current_scene(new_scene: str) -> None:
        """
        Changes the value of the SceneManager in tleng2/core_engine/scene_manager.py
        """
        
        SceneManagerProperties._waiting_scene = new_scene
        SceneManagerProperties._changing_scenes = True


    @staticmethod
    def update_scene():
        if SceneManagerProperties._changing_scenes:
            SceneManagerProperties._current_scene = SceneManagerProperties._waiting_scene
            
            params = RendererProperties.type_parameters[RendererProperties.scene_parameters[SceneManagerProperties._current_scene]]
            RendererProperties._display = params['display']
            RendererProperties._local_default_camera = params['camera']
            
            SceneManagerProperties._changing_scenes = False


class RendererMethods:
    """
    Renderer Static methods that might be needed across the base game.
    """
    @staticmethod
    def import_scene_renderer_params(params_key: str, params: dict) -> None:
        RendererProperties.type_parameters.update({params_key: params})

    
    @staticmethod
    def import_scene_renderer_params_list(params:dict) -> None:
        params_keys = params.keys()
        for key in params_keys:
            RendererProperties.type_parameters.update({key: params[key]})


    @staticmethod
    def clear_render_calls() -> None:
        RendererProperties.render_calls = []


    @staticmethod
    def load_displays() -> None:
        """
        Initialize the display fast.
        """
        RendererProperties._default_display = pygame.Surface(GlobalSettings._disp_res) 
        RendererProperties._window = pygame.display.set_mode(GlobalSettings._win_res)
        RendererProperties.type_parameters.update({'default':{
                                                        'display' : RendererProperties._default_display.copy(),
                                                        'camera' : None 
                                                    }
                                                  })


    @staticmethod
    def load_local_display(width, height) -> pygame.SurfaceType:
        ...


    @staticmethod
    def load_local_display_ratio(ratio) -> pygame.SurfaceType:
        return pygame.Surface((GlobalSettings._win_res[0]*ratio, GlobalSettings._win_res[1]*ratio)) 


    @staticmethod
    def lazy_upscale_display(new_res: tuple[int,int] = GlobalSettings._win_res) -> None:
        """
        Scaling the display to the size of the window.
        And updates the window with the upscale.
        Warning may be very pixelated.
        """
        __temp_disp = pygame.transform.scale(EngineProperties._display, new_res)
        EngineProperties._window.blit(__temp_disp, (0, 0))


    @staticmethod
    def update_window() -> None:
        """
        UpScales or DownScales the display to fit the window. 
        Warning, this might strect the render. 
        """
        
        RendererProperties._window.blit(pygame.transform.scale(RendererProperties._display, RendererProperties._window.get_size()),(0,0))


    @staticmethod
    def update_window_exp(display: pygame.SurfaceType) -> None:
        """
        UpScales or DownScales the display to fit the window. 
        Warning, this might stretch the render. 
        """
        temp_disp = display if display != None else RendererProperties._display
        RendererProperties._window.blit(pygame.transform.scale(temp_disp, RendererProperties._window),(0,0))


    @staticmethod
    def update_window_disp() -> None:
        """
        Updates the window from _display immedietely. Faster than `RendererMethods.update_window()`
        """
        RendererProperties._window.blit(RendererProperties._display, (0, 0))


    @staticmethod
    def fill_display(color: tuple[int, int, int]) -> None:
        """
        Fill the display with color.
        """
        RendererProperties._display.fill(color)


    @staticmethod
    def load_window(
            flags: int = 0,
            depth: int = 0,
            display: int = 0,
            vsync: int = 0
        ) -> None:
        """
        Initialize the window, with added parameters.
        """
        EngineProperties._window = pygame.display.set_mode(GlobalSettings._win_res, flags, depth, display, vsync)


    @staticmethod
    def load_display(): #TODO
        EngineProperties._display = pygame.display.set_mode(GlobalSettings._disp_res)
