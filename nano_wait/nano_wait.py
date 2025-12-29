import time
from .core import NanoWait
from .utils import log_message, get_speed_value
from .vision import VisionMode, VisualState


def wait(
    t: float | None = None,
    *,
    until: str | None = None,
    icon: str | None = None,
    region=None,
    timeout: float = 15.0,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False
) -> VisualState | float:
    """
    Smart wait — time OR visual state.

    Examples:
        wait(2)
        wait(until="logged_in")
        wait(icon="ok.png", timeout=10)
    """

    nw = NanoWait()
    vision = VisionMode()

    speed_value = (
        nw.smart_speed(wifi) if smart else get_speed_value(speed)
    )

    start = time.time()

    # --------------------------------------
    # 🔹 VISUAL WAIT
    # --------------------------------------

    if until or icon:
        while time.time() - start < timeout:

            if until:
                state = vision.detect_text_state(region)
                if state.detected and state.name == until:
                    if verbose:
                        print(f"[NanoWait] 🧠 Estado '{until}' detectado")
                    return state

            if icon:
                state = vision.detect_icon_state(icon, region)
                if state.detected:
                    if verbose:
                        print(
                            f"[NanoWait] 🧠 Ícone '{icon}' detectado "
                            f"(conf={state.confidence})"
                        )
                    return state

            factor = (
                nw.compute_wait_wifi(speed_value, wifi)
                if wifi else
                nw.compute_wait_no_wifi(speed_value)
            )

            poll = max(0.05, min(0.5, 1 / factor))
            time.sleep(poll)

        raise TimeoutError("Visual state não detectado")

    # --------------------------------------
    # 🔹 TIME WAIT (modo antigo)
    # --------------------------------------

    factor = (
        nw.compute_wait_wifi(speed_value, wifi)
        if wifi else
        nw.compute_wait_no_wifi(speed_value)
    )

    wait_time = round(max(0.05, min(t / factor, t)), 3)

    if verbose:
        print(
            f"[NanoWait] ⏱ mode=time | speed={speed_value:.2f} | "
            f"factor={factor:.2f} | wait={wait_time:.3f}s"
        )

    if log:
        log_message(
            f"mode=time speed={speed_value:.2f} "
            f"factor={factor:.2f} wait={wait_time:.3f}s"
        )

    time.sleep(wait_time)
    return wait_time
