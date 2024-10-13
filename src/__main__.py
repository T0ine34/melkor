import argparse
import sys
import os


from gamuLogger import Logger, LEVELS

try:
    from .settings import Settings
    from .engine import importFiles, runTests
    from .customTypes import TestList, Test, Suite
except ImportError:
    from settings import Settings
    from engine import importFiles, runTests
    from customTypes import TestList, Test, Suite
    

Logger.setModule("melkor")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="Path to the configuration file")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
    
    Settings.setFilePath(args.configFile)
        
    testDir = Settings().get("testDir")
    if not os.path.exists(testDir):
        Logger.error(f"Test directory '{testDir}' not found")
        sys.exit(1)

    TestList.new(Settings().get("name"))

    files = [os.path.join(testDir, file) for file in os.listdir(testDir) if file.endswith(".py")]
    modules = importFiles(files)
    
    TestList.getInstance().run()
    Logger.info(str(TestList.getInstance()))
        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.critical(f"An exception occurred: {e}")
