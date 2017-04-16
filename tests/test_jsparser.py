from vcscheck.jsparser import JSParser
import helper
import pytest


def test_equal():
    parser = JSParser()
    code = b'''var a;
function test()
{
    console.info("test");
}'''
    assert list(helper.splitlines(code)) == list(
        helper.test_parser(parser, code))


def test_additional():
    parser = JSParser()
    before = b'''function a() {
    console.info("test");
}'''
    after = b'''function a()
{
    console.info("test");
}
'''
    assert b"".join(helper.splitlines(after)) == b"".join(
        helper.test_parser(parser, before))


@pytest.mark.xfail
def test_removal():
    parser = JSParser()
    before = b'''function a()
{
    console.info("test");


}'''
    after = b'''function a()
{
    console.info("test");
}'''
    assert b"".join(helper.splitlines(after)) == b"".join(
        helper.test_parser(parser, before))
