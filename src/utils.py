from typing import Callable
import builtins


class CapturePrint:
    def __init__(self):
        self.__stdout = []
        
    def __enter__(self):
        self.__buildinPrint = builtins.print
        builtins.print = self.__print
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.print = self.__buildinPrint
        
    def __print(self, *args, **kwargs):
        self.__stdout.append(" ".join(args))
        
    def get(self):
        return self.__stdout