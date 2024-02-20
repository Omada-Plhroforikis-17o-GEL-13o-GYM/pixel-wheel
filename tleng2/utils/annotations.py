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

# # This is used in places where ints are strictly required
# IntCoordinate = Sequence[int]

# # This typehint is used when a function would return an RGBA tuple
# RGBAOutput = Tuple[int, int, int, int]
# ColorValue = Union[int, str, Sequence[int]]

# _CanBeRect = Sequence[Union[float, Coordinate]]

# class _HasRectAttribute(Protocol):
#     # An object that has a rect attribute that is either a rect, or a function
#     # that returns a rect confirms to the rect protocol
#     rect: Union[RectValue, Callable[[], RectValue]]

# RectValue = Union[_CanBeRect, _HasRectAttribute]