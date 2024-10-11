from gamuLogger import Logger

Logger.setModule("melkor")

class UnitTest:
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
