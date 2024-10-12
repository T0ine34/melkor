from gamuLogger import Logger
from enum import Enum

try:
    from .utils import CapturePrint
except ImportError:
    from utils import CapturePrint

Logger.setModule("melkor")


class Tests:
	UNIT = []
	INTEGRATION = []
	END_TO_END = []
 
 
class _testclassdecoratorBase:
	def __init__(self, func):
		self.__func = func
		self.__call__.__annotations__["name"] = func.__name__
		Logger.debug(f"Registered test {self.__func.__name__}")
  
	def __call__(self, *args, **kwargs):
		Logger.debug(f"Running test {self.__func.__name__}")
   
		exitData = {
			"hasSucceeded": True,
			"exception": None
		}
		result = None
		try:
			capture = CapturePrint()
			with capture:
				result = self.__func(*args, **kwargs)
		except Exception as e:
			exitData["exception"] = e
			exitData["hasSucceeded"] = False

		if type(result) == int and result != 0:
			exitData["hasSucceeded"] = False
			exitData["exception"] = Exception(f"Test returned {result}")
	
			
		exitData["output"] = capture.get()
	
		return exitData


def UnitTest(allowedToFail=False):
	class _unittestclassdecorator(_testclassdecoratorBase):
		def __init__(self, func):
			super().__init__(func)
			Tests.UNIT.append(self.__call__)
			
		def __call__(self, *args, **kwargs):
			data = super().__call__(*args, **kwargs)
			data["allowedToFail"] = allowedToFail

			return data

	return _unittestclassdecorator


def IntegrationTest(allowedToFail=False):
	class _integrationtestclassdecorator(_testclassdecoratorBase):
		def __init__(self, func):
			super().__init__(func)
			Tests.INTEGRATION.append(self.__call__)
			
		def __call__(self, *args, **kwargs):
			data = super().__call__(*args, **kwargs)
			data["allowedToFail"] = allowedToFail

			return data

	return _integrationtestclassdecorator


def EndToEndTest(allowedToFail=False):
	class _endtoendtestclassdecorator(_testclassdecoratorBase):
		def __init__(self, func):
			super().__init__(func)
			Tests.END_TO_END.append(self.__call__)
			
		def __call__(self, *args, **kwargs):
			data = super().__call__(*args, **kwargs)
			data["allowedToFail"] = allowedToFail

			return data

	return _endtoendtestclassdecorator
    


