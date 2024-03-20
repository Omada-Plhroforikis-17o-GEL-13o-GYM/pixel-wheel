import json
from os import path, getcwd
from abc import abstractmethod, ABC
# from .debug import debug_print

debug_tags = ['JSON_debug']

class LocalSettings:
    @abstractmethod
    def __init__(self):
        """
        Put the local specific setting that you want the scene/enviroment/object to have
        e.x. (pseudo code)

        self.fps = 30
        self.font = comic_sans
        self.debug = True
        self.test = False
        """

class GlobalSettings:
    """
    Global settings, used across the game.
    """

    _win_res = (1280,720)
    _disp_res = (1280,720)
    _display_scaling = 1
    _scalable_window = False
    _display_ratio_lock = True #if the game only supports 500x500 then the window will ony scale to that ration
    _fps = 60
    _physics_target_fps = 60 # for dt dependant values (delta-time)

    _font = None # global font for the whole game.
    _debug = False

    _jsettings = {}

    # _platform = 'pc' # on what platform is the game for, if for mobile then the display should be changed
    @staticmethod
    def update_bresolution(new_res:tuple[int,int]) -> None:
        """
        Updates the variable of the resolution of *both* the window, and the display.
        It doesn't update the surfaces themselves.
        """
        GlobalSettings._win_res = new_res
        GlobalSettings._disp_res = new_res


    @staticmethod
    def load_settings_json():
        """
        Pass the saved settings from json.
        """
        for file_name in ["settings.json", path.join("..","settings.json") ,path.join("tleng2","settings.json"), path.join(getcwd(), "tleng2","settings.json")]:
            try:
                with open(file_name, "r") as settings_json:
                    data = json.load(settings_json)
                    #debug_print(data, tags=debug_tags)
                    # TODO: Write the load_settings_json to actually use the settings that are in json.
                    break
            except Exception as e:
                #debug_print(e, tags=debug_tags)
                #debug_print(f"Could not find the settings.json file, moving on. (Tried {file_name})", tags=debug_tags)
                #debug_print(path.exists(file_name), tags=debug_tags)
                ...

