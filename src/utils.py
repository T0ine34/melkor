import builtins
import traceback


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
    
    
def formatTraceback(exception: Exception) -> str:
    """Format the traceback of an exception, removing the first element"""
    trace =  traceback.TracebackException.from_exception(exception)
    trace.stack.pop(0)
    return "    ".join(trace.format())