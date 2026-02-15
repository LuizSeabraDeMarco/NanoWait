import time
from nano_wait.nano_wait import wait


def test_wait_respects_minimum_time():
    start = time.time()
    wait(lambda: False, timeout=0.2)
    elapsed = time.time() - start
    assert elapsed >= 0.05


def test_wait_condition_true_immediately():
    start = time.time()
    wait(lambda: True, timeout=1)
    elapsed = time.time() - start
    assert elapsed < 0.1


def test_wait_timeout_expires():
    start = time.time()
    wait(lambda: False, timeout=0.3)
    elapsed = time.time() - start
    assert elapsed >= 0.3


def test_wait_returns_true_when_condition_met():
    result = wait(lambda: True, timeout=1)
    assert result is True


def test_wait_returns_false_on_timeout():
    result = wait(lambda: False, timeout=0.2)
    assert result is False


def test_wait_with_non_callable_condition():
    try:
        wait(True, timeout=0.1)
    except Exception as e:
        assert isinstance(e, TypeError)


def test_wait_timeout_zero():
    result = wait(lambda: False, timeout=0)
    assert result is False
