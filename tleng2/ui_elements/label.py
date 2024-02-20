from ..engine.area import Area
from ..utils.colors import WHITE, BLACK
from ..utils.settings import GlobalSettings
from warnings import warn
import pygame

#TODO: K.I.S.S. (Keep It Simple, Stupid)!!!

class Label(Area):
    '''
    Label is a class for displaying text.
    '''

    def __init__(self, window:pygame.Surface, text:str|list, x:float = 0, y:float = 0, width:float = 10.0, height:float = 10.0,  color:tuple = WHITE,
                 tfont='verdana', tsize:int=12, tcolor:tuple=BLACK, tantialias:bool = True, tbold:bool=False, titalic:bool=False, escape_text:bool=False, 
                 dynamic_change:str|None=None, final_text:list|None=None) -> None:
        '''
        Changing/Creating the text and it's properties, and storing the new text values in class variables 
        (t in front of the word stands for text)\n

        param `window` : It is the window that you want the area to be drew at (pygame Surface) \n
        param `x` : The Horizontal coordinate (float) \n
        param `y` : The Vertical coordinate (float) \n
        param `width` : The width of the area (float) \n
        param `height` : The height of the area (float) \n
        param `color` : The color of the Area (tuple) \n
        param `text` : Type the text you want to store \n
        param `tsize` : It's the desired size for your text (default size 12) \n
        param `tcolor` : It's the desired color for your text (default color BLACK) \n
        param `tbold` : If you want for your text to be bold set it to True (default to False) \n
        param `escape_text` : If you want to output the text raw or edited with this symbol ' \\ ' (currently supported: \\n) \n
        param `dynamic_change` : A function which will be called to handle what happens when the text reaches the edge of the screen, 
                                str = 'default' for the default handling, if there are spaces in the text, then it will make a new line from the words \n
                                None = nothing
        `return` : it returns nothing \n
        '''

        Area.__init__(self, window, x, y, width, height, color)
        self.text_size = tsize
        self.text_color = tcolor
        self.text_bold = tbold
        self.text_italic = titalic
        
        self.escape_text = escape_text

        self.text = text
        self.final_text = final_text # if the user wants to input a complete text, do it here: {class_name_Label}.final_text = [[...,...],[...,...,...]] 
                               # It will be automatically checked, needs to be transformed to Font class befare displaying
        self.multitext = []
        self.font = pygame.font.SysFont(tfont, tsize, tbold, titalic)

        # TODO : Make this more safe (try, except function fails, key fails (KeyError))
        dynamic_preset_dict = {
            'default' : self.words_warp,
        }

        if type(dynamic_change) == str:
            self.dynamic_lines = dynamic_preset_dict[dynamic_change]
        else:
            self.dynamic_lines = dynamic_change

        if escape_text:
            self.multitext = self.newline_text(self.text, self.font, tcolor, tantialias)
        else:
            self.text = self.font.render(self.text, tantialias, self.text_color)

        self.height = self.font.get_height()

    def fusing_lists(self, text:list|tuple) -> str:
        '''
        Fusing a list or tuple into a singular string

        param `text` : Can either be a list or a tuple, the wanted text to be fused from a list/tuple to a string 
        `return` : it returns a fused string of the bigger list
        '''
        text2 = ''
        for i in text:
            if type(i) != list|tuple:
                text2 += str(i)
            else:
                text2 += self.fusing_lists(i)
        return text2
    
    def newline_text(self, text:str|list, font:pygame.font.Font, tcolor:tuple = WHITE, anti_alias:bool = True) -> list:
        '''
        A function that creates a list with every object inside it being a new line

        param `text` : The text of that needs to be checked\n
        param `font` : The font of the text\n
        param `tcolor` : The color of the text\n
        `return` The list of the new cutted words

        '''
        temp_list = []
        # Efficient new text displaying

        if hasattr(self,'text_color'): # if the self attribute has (returns True)
            text_color = self.text_color
        else:
            warn("The label has not been initialized, using color given/default (white)")
            text_color = tcolor

        if hasattr(self,'font'): # if the self attribute has (returns True)
            text_font = self.font
        else:
            warn("The label has not been initialized, using font given/default pygame.font.SysFont('verdana', 12)")
            text_font = font

        if type(text) == list: #checks if the txt is a list or something else hopefully an str
            multitext = self.fusing_lists(text).split('\n')
        else:
            multitext = text.split('\n')
        
        for i in multitext:
            temp_list += text_font.render(str(i), anti_alias, text_color)

        multitext = temp_list

        del temp_list # deleting the temp_list because why not

        return multitext
    
    # WORDS WRAP, there are a lot of different ways you can control the words dynamically changing when they are close to the edge of the window.
    #   The developer is encouraged to write his own code here, or make a function 

    def words_warp(self, multi_text:str|list, font:pygame.font.Font, tcolor:tuple = WHITE, anti_alias:bool = True) -> list:
        space_list = []

        if hasattr(self,'multitext'): # if the self attribute has (returns True)
            multitext = self.multitext
        else:
            warn("The label has not been initialized, using multi_text given")
            multitext = multi_text

        # for performance let's use the self.text to avoid the space iteration

        for i in multitext:
            space_list += i.split(' ')

    def change_text(self, new_text:str|list, tcolor:tuple=BLACK, tantialias:bool = True, escape_text:bool=True, dynamic_change:str|None=None)->None:
        '''
        Storing the text class in a variable for later usage, The Label is created by using a rectangle 
        To draw the text use drawText

        :param text: Type the text you want to store
        :param tsize: It's the desired size for your text (default size 12)
        :param tcolor: It's the desired color for your text (default color BLACK)
        :param tbold: If you want for your text to be bold set it to True (default to False)
        :return: it returns nothing
        '''

                    # = self.font.render(text, True, tcolor)
        self.height = self.font.get_height()


    def draw_Label(self, shift_x:int|float=0, shift_y:int|float=0, new_text:str|list|None=None) -> None: # it justs draws the text in the screen
        '''
        Draws text in the screen, the class variable final_text needs to have the objects inside already turned to pygame.font.Font 

        param `shift_x` : It's used to know how much it should be shifted in the horizontal axis from the orgin point of a rectangle (default 0) \n
        param `shift_x` : It's used to know how much it should be shifted in the vertical axis from the orgin point of a rectangle (default 0) \n
        param `new_text` : The new text. Can either be a list or an str \n 
        `return` it returns nothing \n
        '''
        if self.final_text != None and self.final_text != []:
            for i in range(len(self.final_text)):
                self.window.blit(self.final_text[i], (self.rect.x + shift_x, self.rect.y + shift_y + i*self.height))
        else:
            if new_text != None and new_text != self.text: #check if the new text is different from the previous one, if it is, then change the multitext variable #todo remove this to an another class function
                self.multitext = self.newline_text(new_text, self.font)

            if self.multitext != []:
                for i in range(len(self.multitext)):
                    self.window.blit(self.multitext[i], (self.rect.x + shift_x, self.rect.y + shift_y + i*self.height))

            else:
                self.window.blit(self.text , (self.rect.x + shift_x, self.rect.y + shift_y))
    
    def update(self, shift_x:int|float=0, shift_y:int|float=0, text:str|None= None, final_text:list|None=None) -> None:
        '''
        Function for the sprite group updating
        '''
        self.final_text = final_text
        self.draw_Label(shift_x,shift_y, text)

class Debug(Label): # TODO: Documentation
    def __init__(self, window:pygame.Surface, x:int|float, y:int|float, width:int|float, height:int|float, debug_text:str|list,  
                 debug_text_font:pygame.font.Font='verdana', debug_text_size:int|float = 12, debug_text_color:str|list = WHITE, 
                 debug_text_bold:bool = False, debug_text_antialias:bool = True, rect_color:tuple=WHITE, debug_escape_text:bool=False, debug_dynamic_text:str|None=None) -> None:
        
        Label.__init__(self, window, debug_text, x, y, width, height, rect_color,debug_text_font, debug_text_size, 
                       debug_text_color, debug_text_antialias, debug_text_bold, debug_escape_text, debug_dynamic_text)
        
        self.set_Label(debug_text, debug_text_size,debug_text_color, debug_text_bold)

    def update(self,x,y, shift_x: int | float = 0, shift_y: int | float = 0, text: str | None = None) -> None:
        self.rect.x, self.rect.y  = x, y
        super().update(shift_x, shift_y, text)