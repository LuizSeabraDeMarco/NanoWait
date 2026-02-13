import time
import queue
from typing import overload
from datetime import datetime
import socket
from .learning import AdaptiveLearning
from .core import NanoWait, PROFILES
from .utils import log_message, get_speed_value
from .exceptions import VisionTimeout
from .explain import ExplainReport
from .telemetry import TelemetrySession
from .dashboard import TelemetryDashboard

_ENGINE = None

def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE

# --------------------------
# Função utilitária internet
# --------------------------
def has_internet(host="8.8.8.8", port=53, timeout=1):
    """Detecta se há internet ativa."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

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
    telemetry: bool = False,
    profile: str | None = None
):
    """
    Adaptive wait function. By default, profile="auto" is used.
    """

    nw = _engine()

    # 🔹 default para auto
    if not profile:
        profile = "auto"

    nw.profile = PROFILES.get(profile, PROFILES["default"])
    learning = AdaptiveLearning(nw.profile.name)

    verbose = verbose or nw.profile.verbose

    context = nw.snapshot_context(wifi)
    cpu_score = context["pc_score"]
    wifi_score = context["wifi_score"]

    telemetry_queue = queue.Queue() if telemetry else None
    if telemetry:
        TelemetryDashboard(telemetry_queue).start()

    telemetry_session = TelemetrySession(
        enabled=telemetry,
        cpu_score=cpu_score,
        wifi_score=wifi_score,
        profile=nw.profile.name,
        queue=telemetry_queue
    )
    telemetry_session.start()

    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

    factor = (
        nw.compute_wait_wifi(speed_value, wifi, context=context)
        if wifi or has_internet()
        else nw.compute_wait_no_wifi(speed_value, context=context)
    )

    raw_wait = t / factor if t else factor
    wait_time = round(max(0.05, min(raw_wait, t or raw_wait)), 3)
    wait_time = nw.apply_profile(wait_time)

    # 🔥 APPLY LEARNED BIAS
    bias = learning.get_bias()
    wait_time *= bias
    wait_time = round(wait_time, 4)

    telemetry_session.record(factor=factor, interval=wait_time)

    if verbose:
        print(
            f"[NanoWait | {nw.profile.name}] "
            f"factor={factor:.2f} "
            f"bias={bias:.3f} "
            f"wait={wait_time:.3f}s"
        )

    if log:
        log_message(
            f"[NanoWait | {nw.profile.name}] "
            f"factor={factor:.2f} "
            f"bias={bias:.3f} "
            f"wait={wait_time:.3f}s"
        )

    telemetry_session.stop()

    try:
        time.sleep(wait_time)
        learning.update(True, raw_wait, wait_time)
    except Exception:
        learning.update(False, raw_wait, wait_time)
        raise

    if explain:
        return ExplainReport(
            requested_time=t,
            final_time=wait_time,
            speed_input=speed,
            speed_value=speed_value,
            smart=smart,
            cpu_score=cpu_score,
            wifi_score=wifi_score,
            factor=factor,
            min_floor_applied=raw_wait < 0.05,
            max_cap_applied=t is not None and raw_wait > t,
            timestamp=datetime.utcnow().isoformat()
        )

    return wait_time
