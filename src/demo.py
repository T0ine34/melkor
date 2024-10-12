from tester import UnitTest, IntegrationTest


@UnitTest()
def test():
    print("Hello World!")
    
@UnitTest()
def test2():
    print("Hello World!")
    raise Exception("This is an exception")


@IntegrationTest()
def test3():
    print("Hello World!")
    return 1

