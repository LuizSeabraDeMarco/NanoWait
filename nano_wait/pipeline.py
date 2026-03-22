# nano_wait/pipeline.py

from typing import List, Callable, Any
from .execution import execute


class Pipeline:
    def __init__(self):
        self.steps: List[Callable] = []

    def add(self, fn: Callable):
        self.steps.append(fn)
        return self

    def run(self):
        results = []

        for step in self.steps:
            result = execute(step)
            results.append(result)

            if not result.success:
                break

        return results