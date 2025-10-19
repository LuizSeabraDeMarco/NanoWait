from .core import NanoWait
from .utils import log_message, get_speed_value

def wait(t: float, wifi: str = None, speed: str | float = "normal", verbose=False, log=False) -> float:
    """
    Adaptive smart wait — replaces time.sleep() with intelligence.

    Args:
        t (float): Base wait time in seconds.
        wifi (str, optional): Wi-Fi SSID to evaluate. Defaults to None.
        speed (str|float): 'slow', 'normal', 'fast', 'ultra', or custom float.
        verbose (bool): Print details. Defaults to False.
        log (bool): Write log to file. Defaults to False.

    Returns:
        float: Wait time executed (seconds).
    """
    speed_value = get_speed_value(speed)
    nw = NanoWait()

    factor = nw.wait_wifi(speed_value, wifi) if wifi else nw.wait_n_wifi(speed_value)
    wait_time = round(max(0.05, min(t / factor, t)), 3)

    if verbose:
        print(f"[NanoWait] 🧠 speed={speed_value}, wait={wait_time:.3f}s")

    if log:
        log_message(f"Wait={wait_time:.3f}s | speed={speed_value}")

    import time
    time.sleep(wait_time)
    return wait_time
