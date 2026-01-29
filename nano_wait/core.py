# core.py
from dataclasses import dataclass
from typing import Optional


# ------------------------
# Execution Profiles
# ------------------------

@dataclass(frozen=True)
class ExecutionProfile:
    name: str
    aggressiveness: float      # multiplicador para intervalos adaptativos
    tolerance: float           # permissividade a falhas temporárias
    poll_interval: float       # base para loops de polling
    verbose: bool              # mostra debug automaticamente


PROFILES = {
    "ci": ExecutionProfile(
        name="ci",
        aggressiveness=0.5,
        tolerance=0.9,
        poll_interval=0.05,
        verbose=True,
    ),
    "testing": ExecutionProfile(
        name="testing",
        aggressiveness=1.0,
        tolerance=0.7,
        poll_interval=0.1,
        verbose=True,
    ),
    "rpa": ExecutionProfile(
        name="rpa",
        aggressiveness=2.0,
        tolerance=0.5,
        poll_interval=0.2,
        verbose=False,
    ),
    "default": ExecutionProfile(
        name="default",
        aggressiveness=1.0,
        tolerance=0.8,
        poll_interval=0.1,
        verbose=False,
    ),
}


# ------------------------
# Core Engine
# ------------------------

class NanoWait:
    def __init__(self, profile: Optional[str] = None):
        import platform

        self.system = platform.system().lower()
        self.profile = PROFILES.get(profile, PROFILES["default"])

        # Wi-Fi setup (best-effort)
        if self.system == "windows":
            try:
                import pywifi
                self.wifi = pywifi.PyWiFi()
                self.interface = self.wifi.interfaces()[0]
            except Exception:
                self.wifi = None
                self.interface = None
        else:
            self.wifi = None
            self.interface = None

    # ------------------------
    # Context collection
    # ------------------------

    def get_pc_score(self) -> float:
        """
        Returns a score from 0–10 based on CPU and memory pressure.
        Higher is better (faster system).
        """
        try:
            import psutil

            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent

            cpu_score = max(0, min(10, 10 - cpu / 10))
            mem_score = max(0, min(10, 10 - mem / 10))

            return round((cpu_score + mem_score) / 2, 2)
        except Exception:
            return 5.0

    def get_wifi_signal(self, ssid: str | None = None) -> float:
        """
        Returns Wi-Fi signal strength as a score from 0–10.
        """
        try:
            if self.system == "windows" and self.interface:
                self.interface.scan()
                import time
                time.sleep(2)

                for net in self.interface.scan_results():
                    if ssid is None or net.ssid == ssid:
                        return max(0, min(10, (net.signal + 100) / 10))

            elif self.system == "darwin":
                import subprocess

                out = subprocess.check_output(
                    [
                        "/System/Library/PrivateFrameworks/Apple80211.framework/"
                        "Versions/Current/Resources/airport",
                        "-I",
                    ],
                    text=True,
                )
                line = [l for l in out.splitlines() if "agrCtlRSSI" in l][0]
                rssi = int(line.split(":")[1].strip())
                return max(0, min(10, (rssi + 100) / 10))

            elif self.system == "linux":
                import subprocess

                out = subprocess.check_output(
                    ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"],
                    text=True,
                )
                for l in out.splitlines():
                    active, name, sig = l.split(":")
                    if active == "yes" or (ssid and name == ssid):
                        return max(0, min(10, int(sig) / 10))
        except Exception:
            pass

        return 5.0

    def snapshot_context(self, ssid: str | None = None) -> dict:
        """
        Captures an immutable snapshot of system context.
        Used for deterministic waits, explain mode and telemetry.
        """
        pc = self.get_pc_score()
        wifi = self.get_wifi_signal(ssid) if ssid else None

        return {
            "pc_score": pc,
            "wifi_score": wifi,
        }

    # ------------------------
    # Smart Context
    # ------------------------

    def smart_speed(self, ssid: str | None = None) -> float:
        """
        Returns an adaptive speed factor (0.5 – 5.0)
        based on system + network conditions.
        """
        context = self.snapshot_context(ssid)
        pc = context["pc_score"]
        wifi = context["wifi_score"] if context["wifi_score"] is not None else 5.0

        risk = (pc + wifi) / 2
        return round(max(0.5, min(5.0, risk)), 2)

    # ------------------------
    # Wait computation (pure math)
    # ------------------------

    def compute_wait_wifi(
        self,
        speed: float,
        ssid: str | None = None,
        *,
        context: dict | None = None,
    ) -> float:
        if context is None:
            context = self.snapshot_context(ssid)

        pc = context["pc_score"]
        wifi = context["wifi_score"] if context["wifi_score"] is not None else 5.0

        risk = (pc + wifi) / 2
        return max(0.2, (10 - risk) / speed)

    def compute_wait_no_wifi(
        self,
        speed: float,
        *,
        context: dict | None = None,
    ) -> float:
        if context is None:
            context = self.snapshot_context()

        pc = context["pc_score"]
        return max(0.2, (10 - pc) / speed)

    # ------------------------
    # Execution profile application
    # ------------------------

    def apply_profile(self, base_wait: float) -> float:
        """
        Adjusts wait time according to the active execution profile.
        """
        return base_wait * self.profile.aggressiveness
