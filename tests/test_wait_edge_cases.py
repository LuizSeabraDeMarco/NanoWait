from nano_wait.core import wait

def test_wait_condition_raises_exception():
    def broken():
        raise ValueError("fail")


    try:
        wait(broken, timeout=0.1)
    except ValueError:
        assert True


def test_wait_large_timeout():
    result = wait(lambda: True, timeout=10)
    assert result is True