import time
import json
from pathlib import Path
from dataclasses import dataclass


# ======================================================
# 🔹 VisionResult — resultado público
# ======================================================

@dataclass
class VisionResult:
    name: str
    detected: bool
    confidence: float = 0.0
    meta: dict | None = None


# ======================================================
# 🔹 VisionPattern
# ======================================================

@dataclass
class VisionPattern:
    id: str
    type: str
    value: str
    state: str
    region: tuple | None
    confidence: float = 1.0
    hits: int = 1


# ======================================================
# 🔹 PatternStore
# ======================================================

class PatternStore:
    def __init__(self, path=None):
        self.path = path or Path.home() / ".nano-wait" / "vision_patterns.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.patterns: list[VisionPattern] = []
        self._load()

    def _load(self):
        if not self.path.exists():
            self._save()

        with open(self.path, "r") as f:
            data = json.load(f)
            self.patterns = [VisionPattern(**p) for p in data.get("patterns", [])]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(
                {"version": 3, "patterns": [p.__dict__ for p in self.patterns]},
                f,
                indent=2
            )

    def match_text(self, text: str, region=None):
        for p in self.patterns:
            if p.type == "text" and p.value.lower() in text.lower():
                if p.region is None or p.region == region:
                    p.hits += 1
                    self._save()
                    return p
        return None

    def add_pattern(self, pattern: VisionPattern):
        self.patterns.append(pattern)
        self._save()


# ======================================================
# 🔹 VisionMode
# ======================================================

class VisionMode:
    def __init__(self, mode="observe", load_patterns=True):
        self.mode = mode
        self.store = PatternStore() if load_patterns else None

    # ------------------------
    # Screen capture
    # ------------------------

    def _capture_screen(self, region=None):
        from PIL import ImageGrab
        import cv2
        import numpy as np

        if region:
            x, y, w, h = region
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        else:
            img = ImageGrab.grab()

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # ------------------------
    # OCR
    # ------------------------

    def capture_text(self, regions=None) -> dict:
        from PIL import ImageGrab, ImageOps
        import pytesseract

        results = {}
        regions = regions or [None]

        for idx, region in enumerate(regions):
            if region:
                x, y, w, h = region
                img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            else:
                img = ImageGrab.grab()

            img = ImageOps.grayscale(img)
            text = pytesseract.image_to_string(img).strip()
            results[region or f"full_{idx}"] = text

        return results

    # ------------------------
    # Observe
    # ------------------------

    def observe(self, regions=None) -> str:
        texts = self.capture_text(regions)
        full_text = " ".join(texts.values())

        if self.store:
            match = self.store.match_text(full_text)
            if match:
                return match.state

        return "unknown"

    # ------------------------
    # Icon detection
    # ------------------------

    def detect_icon(self, icon_path: str, region=None, threshold=0.9) -> VisionResult:
        import cv2
        import numpy as np

        screen = self._capture_screen(region)
        template = cv2.imread(icon_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            raise FileNotFoundError(f"Icon not found: {icon_path}")

        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            h, w = template.shape
            return VisionResult(
                name=Path(icon_path).stem,
                detected=True,
                confidence=round(float(max_val), 3),
                meta={"position": (*max_loc, w, h)}
            )

        return VisionResult(Path(icon_path).stem, False)
