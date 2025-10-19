# nano_wait/__init__.py
from .core import NanoWait
import time

def wait(t: float, wifi: str = None, speed: float = 1.5, verbose: bool = False, log: bool = False):
    # garante que speed é float
    speed = float(speed)
    
    nw = NanoWait()
    if wifi:
        wt = nw.wait_wifi(speed=speed, ssid=wifi)
    else:
        wt = nw.wait_n_wifi(speed=speed)
    
    if verbose:
        print(f"[NanoWait] PC+WiFi wait = {wt:.2f}s")
    
    if log:
        with open("nano_wait.log", "a") as f:
            f.write(f"[NanoWait] wait={wt:.2f}s, requested={t}s\n")
    
    import time
    time.sleep(max(t, wt))
