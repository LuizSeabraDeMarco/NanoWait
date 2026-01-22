# nano_wait_pool.py
import asyncio
from typing import List, Callable, Optional
from .nano_wait_async import wait_async

async def _async_wait_task(
    duration: float,
    wifi: Optional[str],
    speed: str | float,
    smart: bool,
    verbose: bool,
    log: bool,
    explain: bool,
    profile: Optional[str],
    callback: Optional[Callable],
    cancel_if: Optional[Callable[[], bool]] = None
):
    """
    Task wrapper for async wait with conditional cancellation.
    """
    try:
        # Cancela se a condição retornar True antes de iniciar
        if cancel_if and cancel_if():
            if verbose:
                print(f"[NanoWait | {profile}] Skipped wait {duration}s due to cancel condition")
            return None

        # Executa wait_async normalmente
        result = await wait_async(
            t=duration,
            wifi=wifi,
            speed=speed,
            smart=smart,
            verbose=verbose,
            log=log,
            explain=explain,
            profile=profile,
            callback=callback
        )
        return result

    except asyncio.CancelledError:
        if verbose:
            print(f"[NanoWait | {profile}] Wait {duration}s cancelled safely")
        return None


async def wait_pool_async(
    durations: List[float],
    wifi: Optional[str] = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False,
    explain: bool = False,
    profile: Optional[str] = None,
    callback: Optional[Callable] = None,
    cancel_if: Optional[Callable[[], bool]] = None
):
    """
    Dispara múltiplos waits adaptativos em paralelo.
    """
    tasks = [
        _async_wait_task(
            duration=d,
            wifi=wifi,
            speed=speed,
            smart=smart,
            verbose=verbose,
            log=log,
            explain=explain,
            profile=profile,
            callback=callback,
            cancel_if=cancel_if
        )
        for d in durations
    ]
    return await asyncio.gather(*tasks)


def wait_pool(
    durations: List[float],
    wifi: Optional[str] = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False,
    explain: bool = False,
    profile: Optional[str] = None,
    callback: Optional[Callable] = None,
    cancel_if: Optional[Callable[[], bool]] = None
):
    """
    Wrapper síncrono que dispara múltiplos waits adaptativos em paralelo usando asyncio.
    """
    return asyncio.run(wait_pool_async(
        durations=durations,
        wifi=wifi,
        speed=speed,
        smart=smart,
        verbose=verbose,
        log=log,
        explain=explain,
        profile=profile,
        callback=callback,
        cancel_if=cancel_if
    ))
