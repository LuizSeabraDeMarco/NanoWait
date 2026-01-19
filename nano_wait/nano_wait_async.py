# nano_wait_async.py
import asyncio
from datetime import datetime

from .core import NanoWait, PROFILES
from .utils import get_speed_value, log_message
from .telemetry import TelemetrySession
from .explain import ExplainReport

_ENGINE = None

def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE

async def wait_async(
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
    profile: str | None = None,
    callback: None | callable = None   # <-- novo
):
    """
    Async adaptive wait with optional explainable execution and callbacks.
    Compatible with FastAPI, bots, scraping async tasks.
    """

    nw = _engine()

    if profile:
        nw.profile = PROFILES.get(profile, PROFILES["default"])

    verbose = verbose or nw.profile.verbose

    # ------------------------
    # Context snapshot
    # ------------------------
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

    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

    # --------------------------------------
    # Visual wait (async using threads)
    # --------------------------------------
    if until or icon:
        from .vision import VisionMode

        vision = VisionMode()
        start = datetime.utcnow().timestamp()

        while datetime.utcnow().timestamp() - start < timeout:
            if until:
                state = await asyncio.to_thread(vision.observe, [region] if region else None)
                if state == until:
                    telemetry_session.stop()
                    result = await asyncio.to_thread(vision.detect_icon, "", region)
                    # Callback após detecção
                    if callback:
                        if asyncio.iscoroutinefunction(callback):
                            await callback()
                        else:
                            await asyncio.to_thread(callback)
                    return result

            if icon:
                result = await asyncio.to_thread(vision.detect_icon, icon, region)
                if result.detected:
                    telemetry_session.stop()
                    # Callback após detecção
                    if callback:
                        if asyncio.iscoroutinefunction(callback):
                            await callback()
                        else:
                            await asyncio.to_thread(callback)
                    return result

            factor = (
                nw.compute_wait_wifi(speed_value, wifi, context=context)
                if wifi else nw.compute_wait_no_wifi(speed_value, context=context)
            )
            interval = max(0.05, min(0.5, 1 / factor))
            interval = nw.apply_profile(interval)

            telemetry_session.record(factor=factor, interval=interval)
            await asyncio.sleep(interval)

        telemetry_session.stop()
        from .exceptions import VisionTimeout
        raise VisionTimeout("Visual condition not detected")

    # --------------------------------------
    # Time wait
    # --------------------------------------
    factor = (
        nw.compute_wait_wifi(speed_value, wifi, context=context)
        if wifi else nw.compute_wait_no_wifi(speed_value, context=context)
    )

    raw_wait = t / factor if t else factor
    wait_time = round(max(0.05, min(raw_wait, t or raw_wait)), 3)
    wait_time = nw.apply_profile(wait_time)

    min_floor_applied = raw_wait < 0.05
    max_cap_applied = t is not None and raw_wait > t

    telemetry_session.record(factor=factor, interval=wait_time)

    if verbose:
        print(f"[NanoWait | {nw.profile.name}] async wait={wait_time:.3f}s factor={factor:.2f}")

    if log:
        log_message(f"[NanoWait | {nw.profile.name}] async wait={wait_time:.3f}s factor={factor:.2f}")

    # ------------------------
    # Execute wait
    # ------------------------
    await asyncio.sleep(wait_time)

    # Executa callback após tempo
    if callback:
        if asyncio.iscoroutinefunction(callback):
            await callback()
        else:
            await asyncio.to_thread(callback)

    telemetry_session.stop()

    # ------------------------
    # Explain report
    # ------------------------
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
        return report

    return wait_time
