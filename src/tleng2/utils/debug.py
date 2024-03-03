from .settings import GlobalSettings
from ..ui_elements.label import Label
from .colors import WHITE
import pygame

def debug_print(*values: object, sep: str | None = " ", end: str | None = "\n", file: None = None, flush = False, tags:list = [])->None:
    """
    Print statement that gets called only when the debug of the application is equal to `True`.
    Basically the Print function, but only print when `GlobalSettings._debug == True`
    """
    if GlobalSettings._debug and DebugTags.debug_tags is not []:
        for i in tags:
            if i in DebugTags.debug_tags:
                print(*values, sep=sep, end=end, file=file, flush=flush)
    elif GlobalSettings._debug:
        print(*values, sep=sep, end=end, file=file, flush=flush)

class DebugTags:
    '''
    Stores an active dictionary that upon called it will try to match what the 
    programmer wants to debug and subsequently approve calls that come from that source.
    '''

    debug_tags = []

    @staticmethod
    def import_tags(tags:list) -> None:
        DebugTags.debug_tags += tags  

class ScreenDebug(Label):
    def __init__(self, 
                 window: pygame.Surface, 
                 x: int |float, 
                 y: int | float, 
                 width: int | float, 
                 height: int | float, 
                 debug_text: str | list,  
                 debug_text_font: pygame.font.Font = 'verdana', 
                 debug_text_size: int | float = 12, 
                 debug_text_color: str | list = WHITE, 
                 debug_text_bold: bool = False, 
                 debug_text_antialias: bool = True, 
                 rect_color: tuple = WHITE, 
                 debug_escape_text: bool = False, 
                 debug_dynamic_text: str | None = None
        ) -> None:
        
        Label.__init__(self, 
                       window, 
                       debug_text, 
                       x, 
                       y, 
                       width, 
                       height, 
                       rect_color,
                       debug_text_font, 
                       debug_text_size, 
                       debug_text_color, 
                       debug_text_antialias, 
                       debug_text_bold, 
                       debug_escape_text,
                       debug_dynamic_text)
        
        self.set_Label(debug_text, 
                       debug_text_size,
                       debug_text_color, 
                       debug_text_bold)

    def update(self, 
               x, 
               y, 
               shift_x: int | float = 0, 
               shift_y: int | float = 0, 
               text: str | None = None
        ) -> None:
        self.rect.x, self.rect.y  = x, y
        super().update(shift_x, shift_y, text)


