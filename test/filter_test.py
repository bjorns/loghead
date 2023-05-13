from kuvio.event import Event
from kuvio.filter import LevelFilter, PROCESSED, TERMINATED
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


def test_terminate_all_levels_below_cutoff():
    for i, level in enumerate(ALL_LEVELS):
        subject = LevelFilter(cutoff=level)
        for j in range(i):
            terminate_level = ALL_LEVELS[j]
            event = Event(level=terminate_level, msg=f"testing {terminate_level}")
            status = subject.process(event)
            assert status == TERMINATED


def test_process_all_levels_on_or_above_cutoff():
    for i, level in enumerate(ALL_LEVELS):
        subject = LevelFilter(cutoff=level)
        for j in range(i, len(ALL_LEVELS)):
            pass_level = ALL_LEVELS[j]
            event = Event(level=pass_level, msg=f"testing {pass_level}")
            status = subject.process(event)
            assert status == PROCESSED
