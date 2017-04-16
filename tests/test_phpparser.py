from vcscheck.phpparser import PHPParser
import helper


def test_equal():
    parser = PHPParser()
    code = b'''<?php
$a = 0;
print_r($a);
function a($b)
{
    return 0;
}
'''
    assert list(helper.splitlines(code)) == list(
        helper.test_parser(parser, code))


def test_addition():
    parser = PHPParser()
    before = b'''<?php
function a($b) {
    return 0;
}'''
    after = b'''<?php
function a($b)
{
    return 0;
}'''
    assert b"".join(helper.splitlines(after)) == b"".join(
        helper.test_parser(parser, before))


def test_removal():
    parser = PHPParser()
    before = b'''<?php
function a($b)

{
    return 0;
}'''
    after = b'''<?php
function a($b)
{
    return 0;
}'''
    assert b"".join(helper.splitlines(after)) == b"".join(
        helper.test_parser(parser, before))
