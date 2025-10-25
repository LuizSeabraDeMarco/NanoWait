import time
import pytesseract
import pyautogui
from pynput.mouse import Controller, Button
from PIL import ImageGrab, ImageOps
import re

class VisionMode:
    """
    Classe para captura e interpretação visual da tela.
    Modos disponíveis:
      - "observe": apenas lê e exibe dados detectados.
      - "decision": lê dados e toma decisões automáticas.
      - "learn": registra padrões visuais para uso futuro.
    """

    def __init__(self, mode="observe"):
        self.mode = mode
        self.mouse = Controller()
        print(f"🔍 VisionMode iniciado no modo '{self.mode}'")

    def capture_numbers(self, regions=None):
        results = {}
        if not regions:
            regions = [None]

        for idx, region in enumerate(regions):
            print(f"📸 Capturando região {idx + 1}...")
            if region:
                x, y, w, h = region
                if w <= 0 or h <= 0:
                    raise ValueError("Largura e altura devem ser maiores que 0")
                bbox = (x, y, x + w, y + h)
                img = ImageGrab.grab(bbox=bbox)
            else:
                img = ImageGrab.grab()

            img = ImageOps.grayscale(img)
            text = pytesseract.image_to_string(img)
            print(f"🧠 Texto detectado na região {idx + 1}: {text}")

            match = re.findall(r'\d+', text)
            numbers = [int(m) for m in match] if match else [0]

            results[region or f"full_screen_{idx}"] = numbers

        return results

    def perform_action(self, action):
        if action == "like_post":
            self.mouse.click(Button.left, 2)
            print("❤️ Ação: clique duplo executado.")
        elif action == "skip_post":
            self.mouse.move(100, 0)
            print("⏭ Ação: pulando item.")
        else:
            print(f"⚙️ Ação desconhecida: {action}")

    def run(self, regions=None):
        numbers_per_region = self.capture_numbers(regions)

        if self.mode == "observe":
            for reg, nums in numbers_per_region.items():
                print(f"👁 Região {reg}: números detectados = {nums}")

        elif self.mode == "decision":
            for reg, nums in numbers_per_region.items():
                for number in nums:
                    if number > 1000:
                        self.perform_action("like_post")
                    else:
                        self.perform_action("skip_post")

        elif self.mode == "learn":
            print("📚 Modo aprendizado ativado: coletando dados...")
            for _ in range(3):
                self.capture_numbers(regions)
                time.sleep(2)
        else:
            print(f"❌ Modo '{self.mode}' inválido.")

    # ------------------------
    # Nova função: mark_region
    # ------------------------
    @staticmethod
    def mark_region():
        """
        Captura região usando PyAutoGUI.
        O usuário clica no canto superior esquerdo e inferior direito.
        Retorna (x, y, largura, altura)
        """
        print("📌 Marque a região desejada:")
        print("Clique no canto superior esquerdo da área desejada e pressione Enter...")
        input("Pressione Enter quando estiver pronto...")
        x1, y1 = pyautogui.position()
        print(f"📍 Ponto superior esquerdo: ({x1}, {y1})")

        print("Clique no canto inferior direito da área desejada e pressione Enter...")
        input("Pressione Enter quando estiver pronto...")
        x2, y2 = pyautogui.position()
        print(f"📍 Ponto inferior direito: ({x2}, {y2})")

        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        if w == 0 or h == 0:
            print("❌ Largura ou altura inválida. Tente novamente.")
            return None

        print(f"✅ Região marcada: (x={x}, y={y}, largura={w}, altura={h})")
        return (x, y, w, h)
