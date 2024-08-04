import pywifi
import psutil
import time

class PCAutomation:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.interface = self.wifi.interfaces()[0]

    def get_wifi_signal(self):
        self.interface.scan()
        time.sleep(2)  # Wait for WiFi scan
        scan_results = self.interface.scan_results()

        ssid = "your_wifi_name"  # Replace with your WiFi network name
        signal_strength = -100  # Default value for poor signal

        for network in scan_results:
            if network.ssid == ssid:
                signal_strength = network.signal
                break

        # Convert signal strength to a scale of 0 to 10
        wifi_score = max(0, min(10, (signal_strength + 100) / 10))
        return wifi_score

    def get_pc_score(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        # Convert CPU and memory usage to a scale of 0 to 10
        cpu_score = max(0, min(10, 10 - cpu_usage / 10))
        memory_score = max(0, min(10, 10 - memory_usage / 10))

        # Average score of CPU and memory
        pc_score = (cpu_score + memory_score) / 2
        return pc_score

    def wait_wifi(self, speed):
        pc_score = self.get_pc_score()
        wifi_score = self.get_wifi_signal()

        # Combined risk score
        risk_score = (pc_score + wifi_score) / 2

        # Calculate wait time based on speed and risk score
        wait_time = max(1, 10 - risk_score - (speed - 1))
        return wait_time

    def wait_n_wifi(self, speed):
        pc_score = self.get_pc_score()

        # Calculate wait time based on speed and risk score
        wait_time = max(1, 10 - pc_score - (speed - 1))
        return wait_time

# Example usage
if __name__ == "__main__":
    automation = PCAutomation()
    wait_time_wifi = automation.wait_wifi(speed=5)
    wait_time_n_wifi = automation.wait_n_wifi(speed=5)
    print(f"Wait Time (with WiFi): {wait_time_wifi} seconds")
    print(f"Wait Time (without WiFi): {wait_time_n_wifi} seconds")
