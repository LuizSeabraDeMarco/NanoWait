import asyncio
from typing import List, Callable, Optional
 
from .nano_wait_async import wait_async
from .utils import log_message
 
 
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
        # (log e callback NÃO são parâmetros de wait_async — tratados abaixo)
        result = await wait_async(
            t=duration,
            wifi=wifi,
            speed=speed,
            smart=smart,
            verbose=verbose,
            explain=explain,
            profile=profile,
        )
 
        if log:
            log_message(f"[NanoWait Pool | {profile}] wait {duration}s -> {result}")
 
        if callback is not None:
            try:
                callback(result)
            except Exception as e:
                if verbose:
                    print(f"[NanoWait | {profile}] callback error: {e}")
 
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
 
    Nota: não pode ser chamado de dentro de um event loop já em execução
    (ex.: dentro de uma função async, ou em notebooks Jupyter). Nesses casos,
    use wait_pool_async() diretamente com `await`.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        pass
    else:
        raise RuntimeError(
            "wait_pool() não pode ser chamado dentro de um event loop já em "
            "execução (ex.: dentro de uma função async ou no Jupyter). "
            "Use 'await wait_pool_async(...)' nesse contexto."
        )
 
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
 