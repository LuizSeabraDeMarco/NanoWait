import time
from typing import Callable, Any, Optional

from .nano_wait import schedule
from .exceptions import VisionTimeout


class ExecutionResult:
    def __init__(self, success: bool, result: Any, attempts: int, duration: float):
        self.success = success
        self.result = result
        self.attempts = attempts
        self.duration = duration

    def __repr__(self):
        return (
            f"<ExecutionResult success={self.success} "
            f"attempts={self.attempts} duration={self.duration:.3f}s>"
        )


def execute(
    fn: Callable,
    *,
    until: Optional[Callable[[Any], bool]] = None,
    retry: bool = True,
    timeout: float = 10.0,
    interval: float = 0.1,
    **kwargs
) -> ExecutionResult:

    start = time.time()
    attempts = 0
    last_error = None

    while True:
        attempts += 1

        try:
            result = fn()

            if not until or until(result):
                return ExecutionResult(
                    True,
                    result,
                    attempts,
                    time.time() - start
                )

        except Exception as e:
            last_error = e

        if not retry:
            return ExecutionResult(False, None, attempts, time.time() - start)

        if time.time() - start > timeout:
            raise VisionTimeout(
                f"Execution timed out after {attempts} attempts"
            ) from last_error

        # 🔥 NanoWait vira scheduler
        schedule(interval, **kwargs)