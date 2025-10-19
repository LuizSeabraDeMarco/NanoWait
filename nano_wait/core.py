import platform
import subprocess
import pywifi
import psutil
import time

class NanoWait:
    def __init__(self):
        self.system = platform.system().lower()
        try:
            if self.system == "windows":
                self.wifi = pywifi.PyWiFi()
                self.interface = self.wifi.interfaces()[0]
            else:
                self.wifi = None
                self.interface = None
        except Exception:
            self.wifi = None
            self.interface = None

    def get_wifi_signal(self, ssid: str) -> float:
        """Get Wi-Fi signal strength (0–10) for Windows, macOS, or Linux."""
        try:
            if self.system == "windows" and self.interface:
                self.interface.scan()
                time.sleep(1.5)
                results = self.interface.scan_results()
                for net in results:
                    if net.ssid == ssid:
                        return max(0, min(10, (net.signal + 100) / 5))
                return 0

            elif self.system == "darwin":  # macOS
                result = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"], capture_output=True, text=True)
                if ssid.lower() in result.stdout.lower():
                    for line in result.stdout.splitlines():
                        if "agrCtlRSSI" in line:
                            signal = int(line.split(":")[1].strip())
                            return max(0, min(10, (signal + 100) / 5))
                return 0

            elif self.system == "linux":
                result = subprocess.run(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if line.startswith(ssid):
                        signal = int(line.split(":")[1])
                        return max(0, min(10, signal / 10))
                return 0

            else:
                return 0

        except Exception:
            return 0
