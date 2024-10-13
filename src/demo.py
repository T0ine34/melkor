from tester import UnitTest, IntegrationTest



def willRaiseException():
    raise Exception("This is an exception")

@UnitTest()
def test():
    print("Hello World!")
    
@UnitTest()
def test2():
    willRaiseException()


@IntegrationTest()
def test3():
    print("Hello World!")
    return 1

