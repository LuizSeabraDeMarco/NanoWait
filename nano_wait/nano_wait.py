# nano_wait.py
import time
from typing import overload
from datetime import datetime

from .core import NanoWait, PROFILES
from .utils import log_message, get_speed_value
from .exceptions import VisionTimeout
from .explain import ExplainReport
from .telemetry import TelemetrySession

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
    explain: bool = False,
    telemetry: bool = False,     # <-- NOVO
    profile: str | None = None
):
    """
    Adaptive deterministic wait with optional explainable execution,
    execution profiles and local experimental telemetry.
    """

    nw = _engine()

    # ------------------------
    # Apply execution profile
    # ------------------------
    if profile:
        nw.profile = PROFILES.get(profile, PROFILES["default"])

    verbose = verbose or nw.profile.verbose

    # ------------------------
    # Context snapshot
    # ------------------------
    context = nw.snapshot_context(wifi)
    cpu_score = context["pc_score"]
    wifi_score = context["wifi_score"]

    # ------------------------
    # Telemetry session (local / opt-in)
    # ------------------------
    telemetry_session = TelemetrySession(
        enabled=telemetry,
        cpu_score=cpu_score,
        wifi_score=wifi_score,
        profile=nw.profile.name,
    )
    telemetry_session.start()

    # ------------------------
    # Speed resolution
    # ------------------------
    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

    # --------------------------------------
    # VISUAL WAIT
    # --------------------------------------
    if until or icon:
        from .vision import VisionMode

        vision = VisionMode()
        start = time.time()

        while time.time() - start < timeout:

            if until:
                state = vision.observe([region] if region else None)
                if state == until:
                    telemetry_session.stop()
                    return vision.detect_icon("", region)

            if icon:
                result = vision.detect_icon(icon, region)
                if result.detected:
                    telemetry_session.stop()
                    return result

            factor = (
                nw.compute_wait_wifi(speed_value, wifi, context=context)
                if wifi else
                nw.compute_wait_no_wifi(speed_value, context=context)
            )

            interval = max(0.05, min(0.5, 1 / factor))
            interval = nw.apply_profile(interval)

            telemetry_session.record(
                factor=factor,
                interval=interval
            )

            time.sleep(interval)

        telemetry_session.stop()
        raise VisionTimeout("Visual condition not detected")

    # --------------------------------------
    # TIME WAIT
    # --------------------------------------
    factor = (
        nw.compute_wait_wifi(speed_value, wifi, context=context)
        if wifi else
        nw.compute_wait_no_wifi(speed_value, context=context)
    )

    raw_wait = t / factor if t else factor
    wait_time = round(max(0.05, min(raw_wait, t or raw_wait)), 3)

    wait_time = nw.apply_profile(wait_time)

    min_floor_applied = raw_wait < 0.05
    max_cap_applied = t is not None and raw_wait > t

    telemetry_session.record(
        factor=factor,
        interval=wait_time
    )

    # ------------------------
    # Verbose / log
    # ------------------------
    if verbose:
        print(
            f"[NanoWait | {nw.profile.name}] "
            f"speed={speed_value:.2f} "
            f"factor={factor:.2f} "
            f"wait={wait_time:.3f}s"
        )

    if log:
        log_message(
            f"[NanoWait | {nw.profile.name}] "
            f"speed={speed_value:.2f} "
            f"factor={factor:.2f} "
            f"wait={wait_time:.3f}s"
        )

    # ------------------------
    # Explain report
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

    telemetry_session.stop()

    # ------------------------
    # Execute wait
    # ------------------------
    time.sleep(wait_time)

    if explain and telemetry:
        return report, telemetry_session.summary()

    if explain:
        return report

    if telemetry:
        return wait_time, telemetry_session.summary()

    return wait_time
