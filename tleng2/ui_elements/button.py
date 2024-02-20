from tleng2.engine.area import *
from tleng2.utils.colors import *
import os  # better performance?
# ______________________________________________________________UI FUNCTIONS _______________________________________________________________________________________

# Button defaults

# IMAGE_NORMAL = pygame.Surface((100, 32))
# IMAGE_NORMAL.fill(pygame.Color('dodgerblue1'))
# IMAGE_HOVER = pygame.Surface((100, 32))
# IMAGE_HOVER.fill(pygame.Color('lightskyblue'))
# IMAGE_DOWN = pygame.Surface((100, 32))
# IMAGE_DOWN.fill(pygame.Color('aquamarine1'))
global indexEvent   
indexEvent = 1

LOCAL_DIRECTORY = os.getcwd()

IMAGE_NORMAL = os.path.join(LOCAL_DIRECTORY,"assets","art","defaults","bttn_normal.png")
IMAGE_HOVER = os.path.join(LOCAL_DIRECTORY,"assets","art","defaults","bttn_hover.png")
IMAGE_DOWN = os.path.join(LOCAL_DIRECTORY,"assets","art","defaults","bttn_clicked.png")
# FONT = pygame.font.SysFont('Comic Sans MS', 32)

class AbstractButton(Area):
    def __init__(self, window, x, y, width, height, color):
        Area.__init__(self, window, x, y, width, height, color)
        pass

class Button(Area):
    '''
    Button class, sub-class of Entity

    The button will be used as, if the the button was pressed, there will be two different states: 
        If pressed button will be in a true false state, more like a switch. And if pressed again will go to the opposite state than it was before
        If pressed and released button, then instead of capturing the true false, it will create an event
    '''
    def __init__(self, 
            window: pygame.Surface, 
            x:float, 
            y:float, 
            button_type:str, 
            width:float, 
            height:float, 
            button_states_path: tuple = (IMAGE_NORMAL,IMAGE_HOVER,IMAGE_DOWN), 
            button_states_txt: tuple = (''),
            color: tuple = LIGHT_GREY, 
            animDict: dict = None, 
            callback = None):
        #json implemantation for buttons, for TlengUtilities

        Area.__init__(self, window, x, y, width, height, color)

        self.state_img = []
        for path in button_states_path:
            self.state_img += [pygame.image.load(path).convert_alpha()]

        self.animations = False
        if animDict != None:
            self.animations = True
            pass
        else:
            self.img_normal = pygame.transform.scale(self.state_img[0],(width, height))
            self.img_hover = pygame.transform.scale(self.state_img[1],(width, height))
            self.img_clicked = pygame.transform.scale(self.state_img[2],(width, height))

        self.image = self.img_normal
        self.button_type = button_type.lower()

        # the coordinates to be able to manipulate the position of the button
        self.X = x
        self.Y = y

        # what will happen when the button is pressed
        self.pressed = False

        global indexEvent
        self.BUTTONPRESSED = pygame.USEREVENT + indexEvent # pygame.event.post(pygame.event.Event(YELLOW_HIT)) <= how to call it in your code
        indexEvent += 1

        # the fucntion that the user wants to be executed when the button is pressed
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.image = self.img_clicked
                    self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.pressed:
                self.callback()
                self.image = self.img_hover
            self.pressed = False

        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.pressed:
                self.image = self.img_hover
            elif not collided:
                self.image = self.img_normal

    def simple_draw(self):
        '''
        Simply just drawing the state of the button
        '''
        print(self.pressed)
        self.window.blit(self.image, (self.X,self.Y))

    def design(self):
        '''
        Designing how the button should look like
        '''
        self.button_design = None
        pass

    def anim_draw(self):
        '''
        A little more advanced version of the function simple_draw()
        '''
        pass