import pywifi
import psutil
import time

class NanoWait:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.interface = self.wifi.interfaces()[0]

    def get_wifi_signal(self, ssid):
        try:
            self.interface.scan()
            time.sleep(2)  # Wait for WiFi scan
            scan_results = self.interface.scan_results()

            signal_strength = -100  # Default value for poor signal

            for network in scan_results:
                if network.ssid == ssid:
                    signal_strength = network.signal
                    break
            else:
                raise ValueError(f"WiFi network '{ssid}' not found.")

            # Convert signal strength to a scale of 0 to 10
            wifi_score = max(0, min(10, (signal_strength + 100) / 10))
            return wifi_score

        except Exception as e:
            print(f"Error getting WiFi signal: {e}")
            return 0

    def get_pc_score(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent

            # Convert CPU and memory usage to a scale of 0 to 10
            cpu_score = max(0, min(10, 10 - cpu_usage / 10))
            memory_score = max(0, min(10, 10 - memory_usage / 10))

            # Average score of CPU and memory
            pc_score = (cpu_score + memory_score) / 2
            return pc_score

        except Exception as e:
            print(f"Error getting PC score: {e}")
            return 0

    def wait_wifi(self, speed, ssid):
        try:
            pc_score = self.get_pc_score()
            wifi_score = self.get_wifi_signal(ssid)

            # Combined risk score
            risk_score = (pc_score + wifi_score) / 2

            # Calculate wait time based on speed and risk score
            wait_time = max(1, (10 - risk_score) / speed)
            return wait_time

        except Exception as e:
            print(f"Error in wait_wifi: {e}")
            return 1

    def wait_n_wifi(self, speed):
        try:
            pc_score = self.get_pc_score()

            # Calculate wait time based on speed and risk score
            wait_time = max(1, (10 - pc_score) / speed)
            return wait_time

        except Exception as e:
            print(f"Error in wait_n_wifi: {e}")
            return 1
