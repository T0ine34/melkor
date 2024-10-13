import xml.etree.ElementTree as ET


try:
    from ..customTypes import Suite, Test, TestList
except:
    from customTypes import Suite, Test, TestList


class Report:
    def __init__(self, TestList: TestList):
        self.__TestList = TestList
    
    def __generateTestElement(self, test: Test) -> ET.Element:
        element = ET.Element("testcase", {
            "name": test.name,
            "time": str(test.time)
        })
        
        if test.failed:
            element.append(ET.Element("failure", {
                "message": test.message
            }))
        elif test.error:
            element.append(ET.Element("error", {
                "message": test.message
            }))
        elif test.skipped:
            element.append(ET.Element("skipped", {
                "message": test.message
            }))
        
        return element
    
    def __generateSuiteElement(self, suite: Suite) -> ET.Element:
        element = ET.Element("testsuite", {
            "name": suite.name,
            "tests": str(suite.tests),
            "failures": str(suite.failures),
            "errors": str(suite.errors),
            "skipped": str(suite.skipped),
            "time": str(suite.time)
        })
        
        for child in suite.childs:
            if isinstance(child, Suite):
                element.append(self.__generateSuiteElement(child))
            else:
                element.append(self.__generateTestElement(child))
        
        return element
    
    def generate(self) -> str:
        root = ET.Element("testsuites")
        root.append(self.__generateSuiteElement(self.__TestList))
        
        return ET.tostring(root, encoding="unicode")
    
    def save(self, path: str):
        with open(path, 'w') as file:
            file.write(self.generate())