# agent.py

from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None

from .nano_wait import wait


class Agent:
    """
    High-level automation agent that observes and acts.
    """

    def __init__(self, vision: bool = False, verbose: bool = False):
        self.verbose = verbose
        self.vision_enabled = vision

    # ------------------------
    # OBSERVE
    # ------------------------
    def observe(self, target: str) -> Optional[tuple]:
        """
        Placeholder for future VisionMode integration.
        """
        if self.verbose:
            print(f"[Agent] Observing: {target}")

        # FUTURE: integrate with nano-wait-vision
        return None

    # ------------------------
    # ACT
    # ------------------------
    def act(self, action: str, target: Optional[str] = None):
        if self.verbose:
            print(f"[Agent] Action: {action} | Target: {target}")

        if action == "click":
            if pyautogui is None:
                raise RuntimeError("pyautogui is required for click actions")

            # fallback simples (centro da tela)
            width, height = pyautogui.size()
            pyautogui.click(width // 2, height // 2)
            return True

        if action == "wait":
            return wait(1)

        return False

    # ------------------------
    # RUN (core)
    # ------------------------
    def run(self, instruction: str):
        """
        Very simple parser (prepare for AI upgrade later)
        """

        instruction = instruction.lower().strip()

        if self.verbose:
            print(f"[Agent] Running: {instruction}")

        if "click" in instruction:
            target = instruction.replace("click", "").strip()
            return self.act("click", target)

        if "wait" in instruction:
            return self.act("wait")

        return {
            "status": "unknown_instruction",
            "instruction": instruction
        }