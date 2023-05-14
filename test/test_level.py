from pytest import raises

from kuvio.error import UserError
from kuvio.level import Level, ALL_LEVELS, DEBUG, INFO, NOTICE, WARNING, ERROR, get_level


def test_level_string_representation():
    assert str(INFO) == "info(20)"


def test_compare_equals_only_cares_about_value():
    foobar_level = Level(INFO.value, "foobar")
    assert foobar_level == INFO


def test_known_levels_in_all_levels():
    assert DEBUG in ALL_LEVELS
    assert INFO in ALL_LEVELS
    assert NOTICE in ALL_LEVELS
    assert WARNING in ALL_LEVELS
    assert ERROR in ALL_LEVELS


def test_relative_ordering():
    assert DEBUG < INFO
    assert INFO < NOTICE
    assert NOTICE < WARNING
    assert WARNING < ERROR


def test_get_level():
    assert get_level('debug') == DEBUG
    assert get_level('info') == INFO
    assert get_level('notice') == NOTICE
    assert get_level('warning') == WARNING
    assert get_level('error') == ERROR

def test_level_doesnt_exist():
    with raises(UserError):
        get_level("doesnt_exist")
