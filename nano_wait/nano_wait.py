import time
from typing import overload
from .core import NanoWait
from .utils import log_message, get_speed_value
from .exceptions import VisionTimeout


_ENGINE = None


def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE


@overload
def wait(t: float, **kwargs) -> float: ...


@overload
def wait(*, until: str, **kwargs): ...


@overload
def wait(*, icon: str, **kwargs): ...


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
):
    nw = _engine()

    speed_value = (
        nw.smart_speed(wifi) if smart else get_speed_value(speed)
    )

    # --------------------------------------
    # VISUAL WAIT (lazy VisionMode)
    # --------------------------------------

    if until or icon:
        from .vision import VisionMode

        vision = VisionMode()
        start = time.time()

        while time.time() - start < timeout:

            if until:
                state = vision.observe([region] if region else None)
                if state == until:
                    return vision.detect_icon("", region)  # dummy result

            if icon:
                result = vision.detect_icon(icon, region)
                if result.detected:
                    return result

            factor = (
                nw.compute_wait_wifi(speed_value, wifi)
                if wifi else
                nw.compute_wait_no_wifi(speed_value)
            )

            time.sleep(max(0.05, min(0.5, 1 / factor)))

        raise VisionTimeout("Visual condition not detected")

    # --------------------------------------
    # TIME WAIT
    # --------------------------------------

    factor = (
        nw.compute_wait_wifi(speed_value, wifi)
        if wifi else
        nw.compute_wait_no_wifi(speed_value)
    )

    wait_time = round(max(0.05, min(t / factor, t)), 3)

    if verbose:
        print(
            f"[NanoWait] speed={speed_value:.2f} "
            f"factor={factor:.2f} wait={wait_time:.3f}s"
        )

    if log:
        log_message(
            f"speed={speed_value:.2f} "
            f"factor={factor:.2f} wait={wait_time:.3f}s"
        )

    time.sleep(wait_time)
    return wait_time
