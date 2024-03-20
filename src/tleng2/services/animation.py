from ..engine.settings import GlobalSettings
from ..utils.properties import GlobalProperties
import pygame

class FancyAnimationService:
    """
    It uses bones instead of multiple images.
    """
    ...


class LazyAnimationService:
    """
    Animation that imports image files immedietly.
    """
    def __init__(self, LocalSettings: None = None):
        self.anim_x = 0
        self.anim_y = 0
        self.anim_dict = {}
        self.current_anim = ''
        self.current_image_anim = ''
        self.anim_frame_data = 0


    def load_animation(self,
            anim_dict:dict
            ) -> None:
        '''
        Load the animation.

        {"%name_anim1%" : {"anim":[str,str,...], "anim_fps" : int}, "%name_anim2%" : {"anim":[str,str,...], "frames" : int}, ...}
        '''
        # self.anim_dict = anim_dict
        temp_anim_keys = anim_dict.keys()
        #looping through the whole dictianary to change them into pygame images
        for key in temp_anim_keys:
            for j in range(len(anim_dict[key])):
                self.new_image = pygame.image.load(anim_dict[key][j]).convert_alpha()
                self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width, self.rect.height)), self.rotation)
                temp_anim_dict += [self.new_image]

            self.anim_dict.update({key: temp_anim_dict}) #updating the entitys animation dict
            temp_anim_dict = [] #resseting the NEW animation list
    

    def import_animation(self,
            anim_dict:dict
            ) -> None:
        self.anim_dict.update(anim_dict)


    def flip_anim(self,key,flip:tuple[bool,bool]=(False,False)) -> list: # TODO: fix this
        temp_anim_dict = self.anim_dict.copy()

        for j in range(len(self.anim_dict[key])):
            temp_anim_dict += [self.new_image]


    def update(self) -> None:
        '''
        Updating the current animation

        :param target_fps: These are the targeted fps, it is useful in case the current fps are 0, then we will use the target_fps
        :param fps: The "wanted" fps of the game (it is advised to use get_fps function as it may not work if you have capped at 1000fps but only get 60)
        :param frames: *How many frames will the animation last
        :return: it returns nothing

        For debugging animation use: 
        print(self.anim[int(self.anim_frame_data)], len(self.anim), self.anim_frame_data, frames, (self.rect.width,self.rect.height))   <----- debugging line
        '''

        # self.window.blit(self.animDict[self.currentAnim][int(self.anim_frame_data)],(self.imageX,self.imageY))
        #(e.x.: 12/60=0.2, every frame its going to be incremented by 0.2, if it is more than the lenght of the animation (4)
        #    then the next image of the animation will play and anim_frame_data will reset)
        current_fps = GlobalProperties._clock.get_fps()
        target_fps = GlobalSettings._fps
        anim_dict_length = len(self.anim_dict[self.current_anim])

        if self.current_anim == "image":
            return None
        
        anim_fps = self.anim_dict[self.current_anim]["anim_fps"]
        if current_fps > 0:
            self.anim_frame_data += anim_fps/current_fps
        else:
            self.anim_frame_data += anim_fps/target_fps #just in case the current_fps hit 0

        if self.anim_frame_data >= anim_dict_length:
            self.anim_frame_data = 0


    def render(self) -> None:
        if self.current_anim == "images":
            GlobalProperties._display.blit(self.anim_dict[self.current_anim][self.current_image_anim], (self.anim_x, self.anim_y))
        else:
            GlobalProperties._display.blit(self.anim_dict[self.current_anim]["anim"][int(self.anim_frame_data)], (self.anim_x, self.anim_y))
