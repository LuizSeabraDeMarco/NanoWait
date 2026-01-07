import time
from typing import overload
from datetime import datetime

from .core import NanoWait
from .utils import log_message, get_speed_value
from .exceptions import VisionTimeout
from .explain import ExplainReport


_ENGINE = None


def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE


# --------------------------------------
# Public API
# --------------------------------------

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
    log: bool = False,
    explain: bool = False
):
    """
    Adaptive deterministic wait with optional explainable execution.
    """

    nw = _engine()

    # ------------------------
    # Context snapshot (single read)
    # ------------------------

    context = nw.snapshot_context(wifi)
    cpu_score = context["pc_score"]
    wifi_score = context["wifi_score"]

    # ------------------------
    # Speed resolution
    # ------------------------

    speed_value = (
        nw.smart_speed(wifi) if smart else get_speed_value(speed)
    )

    # --------------------------------------
    # VISUAL WAIT (VisionMode)
    # --------------------------------------

    if until or icon:
        from .vision import VisionMode

        vision = VisionMode()
        start = time.time()

        while time.time() - start < timeout:

            if until:
                state = vision.observe([region] if region else None)
                if state == until:
                    return vision.detect_icon("", region)

            if icon:
                result = vision.detect_icon(icon, region)
                if result.detected:
                    return result

            factor = (
                nw.compute_wait_wifi(
                    speed_value,
                    wifi,
                    context=context
                )
                if wifi else
                nw.compute_wait_no_wifi(
                    speed_value,
                    context=context
                )
            )

            time.sleep(max(0.05, min(0.5, 1 / factor)))

        raise VisionTimeout("Visual condition not detected")

    # --------------------------------------
    # TIME WAIT
    # --------------------------------------

    factor = (
        nw.compute_wait_wifi(
            speed_value,
            wifi,
            context=context
        )
        if wifi else
        nw.compute_wait_no_wifi(
            speed_value,
            context=context
        )
    )

    raw_wait = t / factor
    wait_time = round(max(0.05, min(raw_wait, t)), 3)

    min_floor_applied = raw_wait < 0.05
    max_cap_applied = raw_wait > t

    # ------------------------
    # Verbose / log
    # ------------------------

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

    # ------------------------
    # Explain report (optional)
    # ------------------------

    report = None
    if explain:
        report = ExplainReport(
            requested_time=t,
            final_time=wait_time,
            speed_input=speed,
            speed_value=speed_value,
            smart=smart,
            cpu_score=cpu_score,
            wifi_score=wifi_score,
            factor=factor,
            min_floor_applied=min_floor_applied,
            max_cap_applied=max_cap_applied,
            timestamp=datetime.utcnow().isoformat()
        )

    # ------------------------
    # Execute wait
    # ------------------------

    time.sleep(wait_time)
    return report if explain else wait_time
