
import asyncio
import time
from typing import Callable, Optional, Union
 
from .learning import AdaptiveLearning
from .core import NanoWait
from .utils import get_speed_value
from .exceptions import WaitTimeoutError
from .nano_wait import _get_engine
 
 
async def wait_async(
    t: Union[float, Callable, None] = None,
    *,
    timeout:          float = 15.0,
    wifi:             Optional[str] = None,
    speed:            Union[str, float] = "normal",
    smart:            bool = False,
    verbose:          bool = False,
    explain:          bool = False,
    profile:          Optional[str] = None,
    raise_on_timeout: bool = False,
) -> Union[float, bool]:
    """
    Espera adaptativa assíncrona (não bloqueia o event loop).
 
    Comportamento garantido (igual ao wait() síncrono):
        wait_async(2)               → espera PELO MENOS 2s
        wait_async(2, smart=True)   → espera adaptativa (pode ser menor)
        wait_async(lambda: x > 0)   → polling até condição ser True ou timeout
 
    Args:
        t:                Tempo (float), condição (callable) ou None para auto.
        timeout:          Timeout máximo para condição callable.
        wifi:             SSID para medição de sinal (opcional).
        speed:            Fator de velocidade: "slow"|"normal"|"fast"|"ultra"|float.
        smart:            Se True, pode reduzir o tempo em sistemas ociosos.
                          Se False (padrão), nunca entrega menos do que o pedido.
        verbose:          Imprime logs de diagnóstico.
        explain:          Retorna dict com detalhes (modo tempo).
        profile:          Perfil de execução.
        raise_on_timeout: Lança WaitTimeoutError se condição não for satisfeita.
 
    Returns:
        float: Tempo real de espera (modo tempo).
        bool:  True se condição satisfeita, False se timeout.
        dict:  Detalhes (quando explain=True e modo tempo).
    """
    # Engine dedicado ao perfil — sem estado compartilhado mutável entre
    # chamadas concorrentes (mesmo padrão do wait() síncrono).
    nw: NanoWait = _get_engine(profile)
 
    learning    = AdaptiveLearning(nw.profile.name)
    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)
 
    # ── MODO CONDIÇÃO ────────────────────────────────────────
    if callable(t):
        if timeout <= 0:
            return False
 
        context  = nw.snapshot_context(wifi)
        start    = time.perf_counter()
        attempts = 0
        bias     = learning.get_bias()
 
        # smart=True aqui de propósito: é o intervalo interno de polling,
        # não um tempo de espera garantido ao usuário.
        base_interval = nw.compute_wait(nw.profile.poll_interval, speed_value, context, smart=True)
        base_interval = max(0.01, min(0.3, base_interval))
 
        while (time.perf_counter() - start) < timeout:
            try:
                # Executa a condição em thread separada para não bloquear o event loop
                result = await asyncio.to_thread(t)
                if result:
                    learning.update(True, 1.0, 1.0)
                    return True
            except Exception as e:
                if verbose:
                    print(f"[NanoWait Async] Condition error (attempt {attempts}): {e}")
 
            elapsed_ratio = min(1.0, (time.perf_counter() - start) / max(timeout, 1))
            interval = base_interval * (1 + elapsed_ratio) * bias
            interval = round(max(0.01, min(0.5, interval)), 4)
 
            if verbose:
                print(
                    f"[NanoWait Async | {nw.profile.name}] "
                    f"Poll #{attempts}: interval={interval:.3f}s"
                )
 
            await asyncio.sleep(interval)
            attempts += 1
 
        learning.update(False, 1.0, 1.0)
 
        if raise_on_timeout:
            raise WaitTimeoutError(
                f"Async condition not met after {timeout}s ({attempts} attempts)."
            )
        return False
 
    # ── MODO TEMPO ───────────────────────────────────────────
    context       = nw.snapshot_context(wifi)
    base_t        = float(t) if t is not None else 1.0
 
    # smart propagado corretamente:
    # - smart=False → nunca entrega menos do que base_t (piso, como no wait() síncrono)
    # - smart=True  → pode reduzir em sistemas ociosos
    adaptive_wait = nw.compute_wait(base_t, speed_value, context, smart=smart)
    adaptive_wait = max(0.005, adaptive_wait)
 
    bias       = learning.get_bias()
    final_wait = round(max(0.005, adaptive_wait * bias), 4)
 
    if verbose:
        mode_label = "smart" if smart else "normal"
        print(
            f"[NanoWait Async | {nw.profile.name} | {mode_label}] "
            f"requested={base_t}s → final={final_wait}s"
        )
 
    await asyncio.sleep(final_wait)
    learning.update(True, base_t, final_wait)
 
    if explain:
        return {
            "requested":    base_t,
            "final":        final_wait,
            "speed_value":  speed_value,
            "bias":         bias,
            "cpu_score":    context["pc_score"],
            "wifi_score":   context["wifi_score"],
            "profile":      nw.profile.name,
        }
 
    return final_wait
 