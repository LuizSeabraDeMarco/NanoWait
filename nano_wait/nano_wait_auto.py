# nano_wait_auto.py
import time
from .core import NanoWait, PROFILES
from .telemetry import TelemetrySession
from .utils import log_message
from .nano_wait import has_internet  # importamos a função

_ENGINE = None

def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE

def wait_auto(
    t: float | None = None,
    *,
    wifi: str | None = None,
    profile: str | None = None,
    verbose: bool = False,
    log: bool = False,
    telemetry: bool = False,
    explain: bool = False
) -> float | dict:

    nw = _engine()

    if profile:
        nw.profile = PROFILES.get(profile, PROFILES["default"])

    verbose = verbose or nw.profile.verbose

    context = nw.snapshot_context(wifi)
    cpu_score = context["pc_score"]
    wifi_score = context["wifi_score"]

    telemetry_session = TelemetrySession(
        enabled=telemetry,
        cpu_score=cpu_score,
        wifi_score=wifi_score,
        profile=nw.profile.name
    )
    telemetry_session.start()

    speed_value = nw.smart_speed(wifi)

    # 🔥 Auto-detect internet aqui
    factor = (
        nw.compute_wait_wifi(speed_value, wifi, context=context)
        if wifi or has_internet()
        else nw.compute_wait_no_wifi(speed_value, context=context)
    )

    interval = max(0.05, 1 / factor)
    interval = nw.apply_profile(interval)

    if t is not None:
        interval = min(interval, t)

    interval = round(interval, 4)

    telemetry_session.record(factor=factor, interval=interval)

    if verbose:
        print(
            f"[NanoWait AUTO | {nw.profile.name}] "
            f"factor={factor:.2f} "
            f"wait={interval:.4f}s"
        )

    if log:
        log_message(
            f"[NanoWait AUTO | {nw.profile.name}] "
            f"factor={factor:.2f} "
            f"wait={interval:.4f}s"
        )

    time.sleep(interval)
    telemetry_session.stop()

    if explain:
        return {
            "interval": interval,
            "factor": factor,
            "cpu_score": cpu_score,
            "wifi_score": wifi_score,
            "profile": nw.profile.name
        }

    return interval
