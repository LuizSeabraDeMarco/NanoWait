class NanoWait:
    def __init__(self):
        import platform
        self.system = platform.system().lower()

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
        import psutil
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            cpu_score = max(0, min(10, 10 - cpu / 10))
            mem_score = max(0, min(10, 10 - mem / 10))
            return round((cpu_score + mem_score) / 2, 2)
        except Exception:
            return 5.0

    def get_wifi_signal(self, ssid: str | None = None) -> float:
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
                        "-I"
                    ],
                    text=True
                )
                line = [l for l in out.splitlines() if "agrCtlRSSI" in l][0]
                rssi = int(line.split(":")[1].strip())
                return max(0, min(10, (rssi + 100) / 10))

            elif self.system == "linux":
                import subprocess
                out = subprocess.check_output(
                    ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"],
                    text=True
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
        This is the foundation for deterministic explain mode.
        """
        pc = self.get_pc_score()
        wifi = self.get_wifi_signal(ssid) if ssid else None

        return {
            "pc_score": pc,
            "wifi_score": wifi
        }

    # ------------------------
    # Smart Context
    # ------------------------

    def smart_speed(self, ssid: str | None = None) -> float:
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
        context: dict | None = None
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
        context: dict | None = None
    ) -> float:
        if context is None:
            context = self.snapshot_context()

        pc = context["pc_score"]
        return max(0.2, (10 - pc) / speed)
