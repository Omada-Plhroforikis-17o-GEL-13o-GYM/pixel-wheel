from pygame import Surface

from dataclasses import dataclass


@dataclass
class Transform:
    x: float
    y: float
    rot: float
    s: int
    # def p


@dataclass
class Button:
    normal: Surface
    hover: Surface
    pressed: Surface
