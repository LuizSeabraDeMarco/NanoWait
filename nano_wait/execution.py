# execution.py

import time
from dataclasses import dataclass
from typing import Callable, Any, Optional

from .nano_wait import schedule


@dataclass
class ExecutionResult:
    success: bool
    result: Any
    attempts: int
    duration: float


def execute(
    fn: Callable,
    *,
    timeout: float = 10.0,
    interval: float = 0.2,
    profile: Optional[str] = None,
    verbose: bool = False
) -> ExecutionResult:
    """
    Repeatedly executes a function until it succeeds or times out.
    """

    start = time.time()
    attempts = 0

    while time.time() - start < timeout:
        try:
            result = fn()

            if result:
                return ExecutionResult(
                    success=True,
                    result=result,
                    attempts=attempts,
                    duration=round(time.time() - start, 3)
                )

        except Exception as e:
            if verbose:
                print(f"[execute] error: {e}")

        schedule(interval, profile=profile)
        attempts += 1

    return ExecutionResult(
        success=False,
        result=None,
        attempts=attempts,
        duration=round(time.time() - start, 3)
    )