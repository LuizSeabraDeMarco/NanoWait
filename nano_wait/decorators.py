from functools import wraps
from .execution import execute


def retry(
    *,
    timeout: float = 10.0,
    interval: float = 0.1,
    **kwargs
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **fn_kwargs):
            return execute(
                lambda: fn(*args, **fn_kwargs),
                timeout=timeout,
                interval=interval,
                **kwargs
            )
        return wrapper

    return decorator