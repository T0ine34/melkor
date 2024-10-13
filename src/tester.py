from gamuLogger import Logger
from enum import Enum
import inspect
import os

try:
	from .utils import CapturePrint, formatTraceback
	from .customTypes import TestList, Test, Suite
	from .settings import Settings
except ImportError:
	from utils import CapturePrint, formatTraceback
	from customTypes import TestList, Test, Suite
	from settings import Settings

Logger.setModule("melkor")

Settings.setFilePath("config.json")
 
class _testclassdecoratorBase:
	def __init__(self, func):
		self.__func = func
		self.__call__.__annotations__["name"] = func.__name__
  
		filepath = os.path.relpath(inspect.getfile(func), Settings().get("testDir"))
		suiteHierarchy = filepath.replace(".py", "").split(os.sep)
		crtSuite = TestList.getInstance()
		for suiteName in suiteHierarchy:
			if not crtSuite.hasChild(suiteName):
				Logger.debug(f"Creating suite {suiteName}")
				crtSuite.addSuite(Suite(filepath, suiteName, crtSuite))
			crtSuite = crtSuite.getChild(suiteName)
		crtSuite.addTest(Test(self.__call__, crtSuite))
  
		Logger.debug(f"Registered test {self.__func.__name__}")
  
	def __call__(self, *args, **kwargs):
		Logger.debug(f"Running test {self.__func.__name__}")
   
		exitData = {
			"hasSucceeded": True,
			"exception": None,
			"traceback": None,
		}
		result = None
		try:
			capture = CapturePrint()
			with capture:
				result = self.__func(*args, **kwargs)
		except Exception as e:
			exitData["exception"] = e
			exitData["hasSucceeded"] = False
			exitData["traceback"] = formatTraceback(e)

		if type(result) == int and result != 0:
			exitData["hasSucceeded"] = False
			exitData["exception"] = Exception(f"Test returned {result}")
	
		exitData["output"] = capture.get()
		return exitData


def UnitTest(allowedToFail=False):
	class _unittestclassdecorator(_testclassdecoratorBase):
		def __init__(self, func):
			super().__init__(func)
			TestList.getInstance().addTest(Test(self.__call__))
			
		def __call__(self, *args, **kwargs):
			data = super().__call__(*args, **kwargs)
			data["allowedToFail"] = allowedToFail

			return data

	return _unittestclassdecorator
