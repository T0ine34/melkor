import argparse
import sys
import os


from gamuLogger import Logger, LEVELS

try:
    from .tester import Tests
    from .settings import Settings
except ImportError:
    from tester import Tests
    from settings import Settings
    

Logger.setModule("melkor")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="Path to the configuration file")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
    
    Settings.setFilePath(args.configFile)
        
    


    totalTests = 0
    failedTests = 0
    globalfailed = False

    
    for testList in [Tests.UNIT, Tests.INTEGRATION, Tests.END_TO_END]:
        listName = "Unit" if testList == Tests.UNIT else "Integration" if testList == Tests.INTEGRATION else "End-to-end"
        if len(testList) == 0:
            continue
        elif globalfailed:
            Logger.info(f"Skipping {len(testList)} {listName} tests because of previous failures")
            continue
        
        Logger.info(f"Running {len(testList)} {listName} tests")
        result = runTests(testList)
        totalTests += result['totalTests']
        failedTests += result['failedTests']
        globalfailed = globalfailed or result['failed']

    
    Logger.info(f"Tests run: {totalTests}, failed: {failedTests}")
        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.critical(f"An exception occurred: {e}")