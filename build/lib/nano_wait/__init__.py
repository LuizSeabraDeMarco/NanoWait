from .core import NanoWait

def wait(t: float, wifi: str = None, speed: float = 1.5, smart: bool = False, verbose: bool = False, log: bool = False):
    """
    Main API function to wait adaptively.
    
    Args:
        t (float): Base wait time in seconds
        wifi (str, optional): Wi-Fi SSID to consider
        speed (float, optional): Speed factor (ignored if smart=True)
        smart (bool, optional): Enable Smart Context Mode
        verbose (bool): Print debug info
        log (bool): Save log
    """
    nw = NanoWait()

    if smart:
        pc_score = nw.get_pc_score()
        wifi_score = nw.get_wifi_signal(wifi) if wifi else 5
        risk_score = (pc_score + wifi_score) / 2
        speed = max(0.5, min(5.0, risk_score))
        if verbose:
            print(f"[Smart Context] PC={pc_score:.2f}, Wi-Fi={wifi_score:.2f}, risk={risk_score:.2f}, speed={speed:.2f}")

    if wifi:
        wait_time = nw.wait_wifi(speed=speed, ssid=wifi)
    else:
        wait_time = nw.wait_n_wifi(speed=speed)

    if verbose:
        print(f"[NanoWait] PC+WiFi wait = {wait_time:.2f}s")

    import time
    time.sleep(wait_time)

    if log:
        with open("nano_wait.log", "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Waited {wait_time:.2f}s\n")
