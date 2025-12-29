import time


class Condition:
    def check(self, vision) -> bool:
        raise NotImplementedError


class Icon(Condition):
    def __init__(self, path, region=None, threshold=0.9):
        self.path = path
        self.region = region
        self.threshold = threshold

    def check(self, vision) -> bool:
        try:
            vision.wait_for_icon(
                self.path,
                region=self.region,
                timeout=0.01,
                threshold=self.threshold,
                poll=0
            )
            return True
        except Exception:
            return False


class Text(Condition):
    def __init__(self, value, region=None):
        self.value = value.lower()
        self.region = region

    def check(self, vision) -> bool:
        texts = vision.capture_text([self.region] if self.region else None)
        full = " ".join(texts.values()).lower()
        return self.value in full


class VisualState:
    def __init__(self, name: str, conditions: list[Condition]):
        self.name = name
        self.conditions = conditions

    def is_ready(self, vision) -> bool:
        return all(cond.check(vision) for cond in self.conditions)
