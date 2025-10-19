import pywifi
import psutil
import time

class NanoWait:
    def __init__(self):
        try:
            self.wifi = pywifi.PyWiFi()
            self.interface = self.wifi.interfaces()[0]
        except Exception:
            self.wifi = None
            self.interface = None

    def get_wifi_signal(self, ssid: str) -> float:
        """Get Wi-Fi signal quality (0–10)."""
        if not self.interface:
            return 0
        try:
            self.interface.scan()
            time.sleep(1.5)
            results = self.interface.scan_results()
            for net in results:
                if net.ssid == ssid:
                    return max(0, min(10, (net.signal + 100) / 5))
            return 0
        except Exception:
            return 0

    def get_pc_score(self) -> float:
        """Get average PC health score (0–10)."""
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            cpu_score = max(0, min(10, 10 - cpu / 10))
            mem_score = max(0, min(10, 10 - mem / 10))
            return (cpu_score + mem_score) / 2
        except Exception:
            return 5

    def wait_wifi(self, speed: float, ssid: str) -> float:
        """Adaptive factor using Wi-Fi + PC."""
        try:
            pc_score = self.get_pc_score()
            wifi_score = self.get_wifi_signal(ssid)
            combined = (pc_score + wifi_score) / 2
            return max(0.5, (10 - combined) / speed)
        except Exception:
            return 1.0

    def wait_n_wifi(self, speed: float) -> float:
        """Adaptive factor using only PC."""
        try:
            pc_score = self.get_pc_score()
            return max(0.5, (10 - pc_score) / speed)
        except Exception:
            return 1.0
