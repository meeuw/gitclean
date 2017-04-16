from vcscheck.pyparser import PyParser
import helper


def test_equal():
    parser = PyParser()
    code = b'''print("hoi")
print("hay")
if True:
    print("blu")


def fun():
    print("bla")
'''
    assert list(helper.splitlines(code)) == list(
        helper.test_parser(parser, code))


def test_additional():
    parser = PyParser()
    before = b'''def fun1():
    pass
def fun2():
    pass
'''
    after = b'''def fun1():
    pass


def fun2():
    pass
'''
    assert list(helper.splitlines(after)) == list(
        helper.test_parser(parser, before))


def test_removal():
    parser = PyParser()
    before = b'''def fun1():
    pass



def fun2():
    pass
'''
    after = b'''def fun1():
    pass


def fun2():
    pass
'''
    assert list(helper.splitlines(after)) == list(
        helper.test_parser(parser, before))
