from tleng2.components.area import Area
from tleng2.utils.colors import WHITE
import pygame, os

LOCAL_DIRECTORY = os.getcwd()

IMAGE_STATE_TRUE = os.path.join(LOCAL_DIRECTORY,"assets","scripts","defaults","bttn_normal.png")
IMAGE_STATE_TRUE_HOVER = os.path.join(LOCAL_DIRECTORY,"assets","scripts","defaults","bttn_hover.png")
IMAGE_STATE_FALSE = os.path.join(LOCAL_DIRECTORY,"assets","scripts","defaults","bttn_clicked.png")
IMAGE_STATE_FALSE_HOVER = os.path.join(LOCAL_DIRECTORY,"assets","scripts",  "defaults","bttn_clicked.png")

class Switch(Area):
    def __init__(self, 
            window, 
            x:float, 
            y:float, 
            width:float, 
            height:float, 
            switchStates:tuple = [
                IMAGE_STATE_FALSE, 
                IMAGE_STATE_FALSE_HOVER, 
                IMAGE_STATE_TRUE, 
                IMAGE_STATE_TRUE_HOVER
                ], 
            color:tuple = WHITE
            ): #dictionaries?
        Area.__init__(self, window, x, y, width, height, color)
        self.switchStates = []
        for path in switchStates:
            self.state_img += [pygame.image.load(path).convert_alpha()]
        self.stateFalse = self.switchStates[0]
        self.stateFalseHover = self.switchStates[1]
        self.stateTrue = self.switchStates[2]
        self.stateTrueHover = self.switchStates[3]