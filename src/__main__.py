import argparse
import sys
import os
import importlib.util

from gamuLogger import Logger, LEVELS

try:
    from .tester import Tests
except ImportError:
    from tester import Tests
    

Logger.setModule("melkor")

def importFile(file):
    spec = importlib.util.spec_from_file_location("module.name", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runTests(testList : list):
    result = {
        'totalTests': len(testList),
        'failedTests': 0,
        'failed': False
    }
    
    for test in testList:
        data = test()
        if not data["hasSucceeded"]:
            result['failedTests'] += 1
            Logger.error(f"Test {test.__annotations__['name']} failed with exception: {data['exception']}")
            if not data["allowedToFail"]:
                result['failed'] = True
        else:
            Logger.info(f"Test {test.__annotations__['name']} succeeded")
    
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file to read")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
    
    if not os.path.exists(args.file):
        print(f"File '{args.file}' not found")
        sys.exit(1)
        
    Logger.info(f"Registering tests from file '{args.file}'")
    module = importFile(args.file)


    totalTests = 0
    failedTests = 0
    globalfailed = False
    
    # Run unit tests
    Logger.info("Running unit tests")
    result = runTests(Tests.UNIT)
    totalTests += result['totalTests']
    failedTests += result['failedTests']
    globalfailed = globalfailed or result['failed']
    
    # Run integration tests
    Logger.info("Running integration tests")
    result = runTests(Tests.INTEGRATION)
    totalTests += result['totalTests']
    failedTests += result['failedTests']
    globalfailed = globalfailed or result['failed']
    
    # Run end-to-end tests
    Logger.info("Running end-to-end tests")
    result = runTests(Tests.END_TO_END)
    totalTests += result['totalTests']
    failedTests += result['failedTests']
    globalfailed = globalfailed or result['failed']
    
    
    Logger.info(f"Tests run: {totalTests}, failed: {failedTests}")
    Logger.info("Tests failed" if globalfailed else "All tests succeeded")
        

if __name__ == "__main__":
    main()