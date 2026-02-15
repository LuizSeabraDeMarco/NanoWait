import asyncio
import time
from datetime import datetime
from typing import Callable, Optional

from .learning import AdaptiveLearning
from .core import NanoWait, PROFILES
from .utils import get_speed_value
from .telemetry import TelemetrySession
from .explain import ExplainReport

_ENGINE = None


def _engine():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait()
    return _ENGINE


async def wait_async(
    t: float | Callable | None = None,
    *,
    timeout: float = 15.0,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    explain: bool = False,
    telemetry: bool = False,
    profile: str | None = None,
):

    nw = _engine()

    if not profile:
        profile = "auto"

    nw.profile = PROFILES.get(profile, PROFILES["default"])
    learning = AdaptiveLearning(nw.profile.name)

    # CONDITION MODE
    if callable(t):

        if timeout <= 0:
            return False

        context = nw.snapshot_context(wifi)
        speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

        start = time.time()

        while time.time() - start < timeout:

            if await asyncio.to_thread(t):
                learning.update(True, 1.0, 1.0)
                return True

            factor = nw.compute_wait_no_wifi(speed_value, context=context)
            interval = max(0.05, min(0.5, 1 / factor))
            interval = nw.apply_profile(interval)

            bias = learning.get_bias()
            interval *= bias
            interval = round(interval, 4)

            await asyncio.sleep(interval)

        learning.update(False, 1.0, 1.0)
        return False

    # NORMAL TIME
    factor = nw.compute_wait_no_wifi(1.0, context=nw.snapshot_context(wifi))
    raw_wait = t / factor if t else factor
    wait_time = round(max(0.05, min(raw_wait, t or raw_wait)), 3)

    await asyncio.sleep(wait_time)
    return wait_time
