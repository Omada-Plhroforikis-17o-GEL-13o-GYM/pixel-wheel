from pygame.math import Vector2
#from pygame._common import RectValue
from typing import IO, Callable, Tuple, Union, TypeVar
from typing_extensions import Literal as Literal, SupportsIndex as SupportsIndex
from typing_extensions import Protocol
from typing import Sequence, Tuple, Union, overload

# Coordinate = Union[Tuple[float, float], Vector2()]
Color = Union[Tuple[int,int,int, int], Tuple[int,int,int]]
# {"%name_anim1%" : {"anim":[str,str,...], "frames" : int}, "%name_anim2%" : {"anim":[str,str,...], "frames" : int}, ...}

Coordinate = Sequence[float]
Vertex = Vector2
VertRect = Sequence[Vertex]