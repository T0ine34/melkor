import datetime


class Test:
    def __init__(self, name : str, failed : bool = False, error : bool = False, skipped : bool = False, time : float = 0.0):
        self.__name = name
        self.__failed = failed
        self.__error = error
        self.__skipped = skipped
        self.__time = time
        self.__message = ""
        
    def setFailed(self, message : str):
        self.__failed = True
        self.__message = message
        
    def setError(self, message : str):
        self.__error = True
        self.__message = message
        
    def setSkipped(self, message : str):
        self.__skipped = True
        self.__message = message
        
    @property
    def name(self):
        return self.__name
    
    @property
    def failed(self):
        return self.__failed
    
    @property
    def error(self):
        return self.__error
    
    @property
    def skipped(self):
        return self.__skipped
    
    @property
    def time(self):
        return self.__time  
    
    @property
    def message(self):
        return self.__message
    

class Suite:
    def __init__(self, file : str, name : str = None):
        self.__name = name if name is not None else file
        self.__timestamp = datetime.datetime.now() # Date and time of when the test run was executed
        self.__childs = []
        self.__tests = 0
        self.__failures = 0
        self.__errors = 0
        self.__skipped = 0
        self.__time = 0.0
        self.__file = file
        
    def addTest(self, test : Test):
        self.__childs.append(test)
        self.__tests += 1
        self.__failures += 1 if test.failed else 0
        self.__errors += 1 if test.error else 0
        self.__skipped += 1 if test.skipped else 0
        self.__time += test.time
        
    def addSuite(self, suite: 'Suite'):
        self.__childs.append(suite)
        self.__tests += suite.tests
        self.__failures += suite.failures
        self.__errors += suite.errors
        self.__skipped += suite.skipped
        self.__time += suite.time
        
    @property
    def name(self):
        return self.__name
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def tests(self):
        return self.__tests
    
    @property
    def failures(self):
        return self.__failures
    
    @property
    def errors(self):
        return self.__errors
    
    @property
    def skipped(self):
        return self.__skipped
    
    @property
    def time(self):
        return self.__time
    
    @property
    def file(self):
        return self.__file
    
    @property
    def childs(self):
        return self.__childs
    



class TestResults:
    def __init__(self, test_name):
        self.__timestamp = datetime.datetime.now() # Date and time of when the test run was executed
        self.__test_name = test_name
        self.__tests = 0
        self.__failures = 0
        self.__errors = 0
        self.__skipped = 0
        self.__time = 0.0
        self.__childs = []
        
    def addTest(self, test : Test):
        self.__childs.append(test)
        self.__tests += 1
        self.__failures += 1 if test.failed else 0
        self.__errors += 1 if test.error else 0
        self.__skipped += 1 if test.skipped else 0
        self.__time += test.time
        
    def addSuite(self, suite: Suite):
        self.__childs.append(suite)
        self.__tests += suite.tests
        self.__failures += suite.failures
        self.__errors += suite.errors
        self.__skipped += suite.skipped
        self.__time += suite.time
        
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def test_name(self):
        return self.__test_name
    
    @property
    def tests(self):
        return self.__tests
    
    @property
    def failures(self):
        return self.__failures
    
    @property
    def errors(self):
        return self.__errors
    
    @property
    def skipped(self):
        return self.__skipped
    
    @property
    def time(self):
        return self.__time
    
    @property
    def childs(self):
        return self.__childs        
    