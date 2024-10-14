from melkor import UnitTest

from engine import importFiles

def willRaiseException():
    raise Exception("This is an exception")

@UnitTest()
def test(): # Will pass
    print("Hello World!")
    
@UnitTest()
def test2(): # Will fail because of the exception
    willRaiseException()


@UnitTest()
def test3(): # Will fail because of the return code != 0
    print("Hello World!")
    return 1


@UnitTest()
def test4(): # Will fail because of the assertion
    assert False