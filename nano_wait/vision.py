import time
import json
from pathlib import Path
from dataclasses import dataclass

import pytesseract
import pyautogui
from pynput.mouse import Controller, Button
from PIL import ImageGrab, ImageOps

import cv2
import numpy as np


# ======================================================
# 🔹 VisualState — engine interna (NÃO quebra API)
# ======================================================

@dataclass
class VisualState:
    name: str
    detected: bool
    confidence: float = 0.0
    meta: dict | None = None


# ======================================================
# 🔹 VisionPattern — padrão aprendido
# ======================================================

@dataclass
class VisionPattern:
    id: str
    type: str               # "text" | "icon"
    value: str              # texto OU caminho do ícone
    state: str
    region: tuple | None
    confidence: float = 1.0
    hits: int = 1


# ======================================================
# 🔹 PatternStore — memória determinística
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
            self.patterns = [
                VisionPattern(**p) for p in data.get("patterns", [])
            ]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(
                {
                    "version": 3,
                    "patterns": [p.__dict__ for p in self.patterns]
                },
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
# 🔹 Template Matching (ícones)
# ======================================================

def _match_icon(template_path, screenshot, threshold=0.9):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Ícone não encontrado: {template_path}")

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(
        screenshot_gray,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape
        return VisualState(
            name=Path(template_path).stem,
            detected=True,
            confidence=round(float(max_val), 3),
            meta={"position": (max_loc[0], max_loc[1], w, h), "type": "icon"}
        )

    return VisualState(Path(template_path).stem, False)


# ======================================================
# 🔹 VisionMode — API pública rica
# ======================================================

class VisionMode:
    """
    Modos conceituais:
      - observe
      - learn
      - decision
    """

    def __init__(self, mode="observe", load_patterns=True):
        self.mode = mode
        self.mouse = Controller()
        self.store = PatternStore() if load_patterns else None
        print(f"🔍 VisionMode iniciado no modo '{self.mode}'")

    # --------------------------------------------------
    # 📸 Captura de tela
    # --------------------------------------------------

    def _capture_screen(self, region=None):
        if region:
            x, y, w, h = region
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        else:
            img = ImageGrab.grab()

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # --------------------------------------------------
    # 📸 OCR
    # --------------------------------------------------

    def capture_text(self, regions=None) -> dict:
        results = {}
        if not regions:
            regions = [None]

        for idx, region in enumerate(regions):
            if region:
                x, y, w, h = region
                bbox = (x, y, x + w, y + h)
                img = ImageGrab.grab(bbox=bbox)
            else:
                img = ImageGrab.grab()

            img = ImageOps.grayscale(img)
            text = pytesseract.image_to_string(img).strip()
            results[region or f"full_{idx}"] = text

        return results

    # --------------------------------------------------
    # 🧠 OBSERVE
    # --------------------------------------------------

    def observe(self, regions=None) -> str:
        texts = self.capture_text(regions)
        full_text = " ".join(texts.values())

        if self.store:
            match = self.store.match_text(full_text)
            if match:
                print(f"🧠 Estado reconhecido: {match.state}")
                return match.state

        return "unknown"

    # --------------------------------------------------
    # 📚 LEARN (texto)
    # --------------------------------------------------

    def learn(self, value: str, state: str, region=None, confidence=1.0):
        if not self.store:
            raise RuntimeError("PatternStore não está ativo")

        pattern = VisionPattern(
            id=f"text_{state}_{len(self.store.patterns)}",
            type="text",
            value=value,
            state=state,
            region=region,
            confidence=confidence
        )

        self.store.add_pattern(pattern)
        print(f"📚 Texto aprendido: {state}")

    # --------------------------------------------------
    # 📚 LEARN (ícone)
    # --------------------------------------------------

    def learn_icon(self, icon_path: str, state: str, region=None, confidence=0.9):
        if not self.store:
            raise RuntimeError("PatternStore não está ativo")

        pattern = VisionPattern(
            id=f"icon_{state}_{len(self.store.patterns)}",
            type="icon",
            value=icon_path,
            state=state,
            region=region,
            confidence=confidence
        )

        self.store.add_pattern(pattern)
        print(f"📚 Ícone aprendido: {state}")

    # --------------------------------------------------
    # ⏱️ WAIT FOR ICON (API ALTA)
    # --------------------------------------------------

    def wait_for_icon(
        self,
        icon_path: str,
        region=None,
        timeout=10.0,
        threshold=0.9,
        poll=0.3
    ):
        start = time.time()

        while time.time() - start < timeout:
            screen = self._capture_screen(region)
            state = _match_icon(icon_path, screen, threshold)

            if state.detected:
                print(
                    f"🧠 Ícone detectado: {icon_path} "
                    f"(confiança={state.confidence})"
                )
                return state

            time.sleep(poll)

        raise TimeoutError(f"Ícone não encontrado em {timeout}s: {icon_path}")

    # --------------------------------------------------
    # ⚙️ ACTIONS
    # --------------------------------------------------

    def perform_action(self, action):
        if action == "like_post":
            self.mouse.click(Button.left, 2)
            print("❤️ Ação: clique duplo.")
        elif action == "skip_post":
            self.mouse.move(100, 0)
            print("⏭ Ação: pular.")
        else:
            print(f"⚙️ Ação desconhecida: {action}")

    # --------------------------------------------------
    # 📌 MARK REGION
    # --------------------------------------------------

    @staticmethod
    def mark_region():
        print("📌 Marque a região:")
        input("Clique no canto superior esquerdo e pressione Enter...")
        x1, y1 = pyautogui.position()

        input("Clique no canto inferior direito e pressione Enter...")
        x2, y2 = pyautogui.position()

        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        if w == 0 or h == 0:
            print("❌ Região inválida")
            return None

        print(f"✅ Região marcada: {x}, {y}, {w}, {h}")
        return (x, y, w, h)
