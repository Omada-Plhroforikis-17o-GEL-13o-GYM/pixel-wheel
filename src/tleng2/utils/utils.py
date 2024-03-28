import os

from math import pi
from time import time
from .debug import debug_print
from ..engine.settings import GlobalSettings

def convert_deg_to_rad(deg) -> float:
    return (deg*pi)/180


def convert_rad_to_deg(rad) -> float:
    return (rad*180)/pi


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


def timer_func_debug(func): 
    # This function shows the execution time of  
    # the function object passed 
    # maybe not so optimized
    def wrap_func(*args, **kwargs): 
        result = None
        if GlobalSettings._debug:
            t1 = time() 
            result = func(*args, **kwargs) 
            t2 = time() 
        else:
            result = func(*args, **kwargs) 

        debug_print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 


def get_parent_dir(path, directories=1):
	path_result = None
	for i in range(directories):
		path_result = get_parent_dir(path.rpartition(os.sep)[0], i)
	return path_result or path