from kuvio.level import ALL_LEVELS, DEBUG, INFO, NOTICE, WARNING, ERROR


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
