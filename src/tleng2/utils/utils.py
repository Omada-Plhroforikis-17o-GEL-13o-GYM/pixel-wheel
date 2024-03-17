from math import pi
from time import time

def convert_deg_to_rad(deg) -> float:
    return (deg*pi)/180


def convert_rad_to_deg(rad) -> float:
    return (rad*pi)/180


def timer_func(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 