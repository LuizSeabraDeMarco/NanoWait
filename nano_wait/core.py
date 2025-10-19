class NanoWait:
    def __init__(self):
        import platform
        self.system = platform.system().lower()
        # Apenas Windows precisa de pywifi
        if self.system == "windows":
            import pywifi
            self.wifi = pywifi.PyWiFi()
            self.interface = self.wifi.interfaces()[0]
        else:
            self.wifi = None
            self.interface = None

    def get_pc_score(self):
        import psutil
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            return (max(0, min(10, 10 - cpu / 10)) + max(0, min(10, 10 - mem / 10))) / 2
        except:
            return 0

    def get_wifi_signal(self, ssid=None):
        # Retorna 0 se Wi-Fi não disponível
        if self.system == "windows" and self.interface:
            try:
                self.interface.scan()
                import time
                time.sleep(2)
                for net in self.interface.scan_results():
                    if ssid is None or net.ssid == ssid:
                        return max(0, min(10, (net.signal + 100) / 10))
            except:
                return 0
        elif self.system == "darwin":
            import subprocess
            try:
                out = subprocess.check_output([
                    "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                    "-I"
                ], text=True)
                line = [l for l in out.split("\n") if "agrCtlRSSI" in l][0]
                rssi = int(line.split(":")[1].strip())
                return max(0, min(10, (rssi + 100) / 10))
            except:
                return 0
        elif self.system == "linux":
            import subprocess
            try:
                out = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"], text=True)
                for l in out.splitlines():
                    active, name, sig = l.split(":")
                    if active == "yes" or (ssid and name == ssid):
                        return max(0, min(10, int(sig)/10))
            except:
                return 0
        return 0

    def wait_wifi(self, speed=1.5, ssid=None):
        """Sempre disponível, mesmo sem pywifi"""
        pc = self.get_pc_score()
        wifi = self.get_wifi_signal(ssid)
        risk = (pc + wifi) / 2
        return max(0.2, (10 - risk)/speed)

    def wait_n_wifi(self, speed=1.5):
        pc = self.get_pc_score()
        return max(0.2, (10 - pc)/speed)
