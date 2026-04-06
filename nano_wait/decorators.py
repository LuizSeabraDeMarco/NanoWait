# decorators.py

from functools import wraps
from .execution import execute


def retry(timeout=5, interval=0.2):
    """
    Retry decorator powered by NanoWait execution engine.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return execute(
                lambda: fn(*args, **kwargs),
                timeout=timeout,
                interval=interval
            )
        return wrapper

    return decorator