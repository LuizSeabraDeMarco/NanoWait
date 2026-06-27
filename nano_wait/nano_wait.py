"""
NanoWait Main API
-----------------
Interface de alto nível para o motor de execução adaptativo.
Suporta esperas baseadas em tempo, condições, telemetria e contexto.

Comportamento garantido:
- wait(2)              → espera PELO MENOS 2s (só aumenta se sistema lento)
- wait(2, smart=True)  → espera adaptativa (pode ser menor em sistema ocioso)
- wait(lambda: x > 0)  → polling inteligente até condição ser True ou timeout
"""

import time
import socket
import threading
from contextlib import contextmanager
from typing import overload, Callable, Optional, Union, Dict, Any
from datetime import datetime

from .learning import AdaptiveLearning
from .core import NanoWait, PROFILES
from .utils import get_speed_value
from .explain import ExplainReport
from .telemetry import TelemetrySession
from .exceptions import WaitTimeoutError

# ──────────────────────────────────────────────
# Motor Singleton por perfil
# ──────────────────────────────────────────────

_ENGINES: Dict[str, NanoWait] = {}
_ENGINES_LOCK = threading.Lock()

def _get_engine(profile: Optional[str] = None) -> NanoWait:
    """
    Retorna (ou cria) um motor NanoWait para o perfil dado.
    Mantém um motor por perfil para evitar contaminação de estado.
    """
    key = profile or "default"
    with _ENGINES_LOCK:
        if key not in _ENGINES:
            _ENGINES[key] = NanoWait(profile)
        return _ENGINES[key]

# ──────────────────────────────────────────────
# Utilitários de Rede
# ──────────────────────────────────────────────

def has_internet(host: str = "8.8.8.8", port: int = 53, timeout: float = 1.0) -> bool:
    """
    Verifica conectividade básica de rede.

    Args:
        host:    IP/host alvo (padrão: Google DNS).
        port:    Porta alvo (padrão: 53/DNS).
        timeout: Timeout da conexão em segundos.

    Returns:
        True se conectado, False caso contrário.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

# ──────────────────────────────────────────────
# Telemetria (helper interno)
# ──────────────────────────────────────────────

def _setup_telemetry(nw: NanoWait, context: Dict[str, Any], enabled: bool) -> TelemetrySession:
    """Configura e inicia uma sessão de telemetria."""
    session = TelemetrySession(
        enabled=enabled,
        cpu_score=context["pc_score"],
        wifi_score=context["wifi_score"],
        profile=nw.profile.name,
        queue=None,
    )
    session.start()
    return session

# ──────────────────────────────────────────────
# API Principal: wait()
# ──────────────────────────────────────────────

@overload
def wait(t: float, **kwargs) -> float: ...
@overload
def wait(until: Callable, **kwargs) -> bool: ...

def wait(
    t: Union[float, Callable, None] = None,
    *,
    timeout:   float = 15.0,
    wifi:      Optional[str] = None,
    speed:     Union[str, float] = "normal",
    smart:     bool = False,
    verbose:   bool = False,
    log:       bool = False,
    explain:   bool = False,
    telemetry: bool = False,
    profile:   Optional[str] = None,
    raise_on_timeout: bool = False,
) -> Union[float, bool, "ExplainReport"]:
    """
    Executa uma espera adaptativa baseada em tempo ou condição.

    Modos:
        wait(2.0)                 → espera pelo menos 2s (pode ser mais se sistema lento)
        wait(2.0, smart=True)     → espera adaptativa (pode ser menos em sistema ocioso)
        wait(lambda: x > 0)      → polling até condição ser True ou timeout
        wait(None)                → espera automática baseada no sistema

    Args:
        t:                Tempo (float) ou condição (callable) ou None para auto.
        timeout:          Tempo máximo de espera para condição (callable).
        wifi:             SSID da rede para medir sinal (opcional). Requer nano-wait[wifi].
        speed:            Fator de velocidade: "slow" | "normal" | "fast" | "ultra" | float.
        smart:            Se True, pode reduzir o tempo em sistemas ociosos.
                          Se False (padrão), nunca entrega menos do que o pedido.
        verbose:          Imprime logs de diagnóstico.
        log:              Salva logs em nano_wait.log.
        explain:          Retorna ExplainReport em vez do tempo de espera.
        telemetry:        Ativa coleta de telemetria em tempo real.
        profile:          Perfil de execução: "ci" | "testing" | "rpa" | "turbo" | "safe".
        raise_on_timeout: Se True, lança WaitTimeoutError quando callable não resolve.

    Returns:
        float:         Tempo real de espera (modo tempo).
        bool:          True se condição satisfeita, False se timeout (modo callable).
        ExplainReport: Relatório detalhado (quando explain=True, modo tempo).
    """
    nw = _get_engine(profile)
    verbose = verbose or nw.profile.verbose

    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

    # ── MODO CONDIÇÃO (CALLABLE) ──────────────────────────────────────
    if callable(t):
        if timeout <= 0:
            return False

        learning = AdaptiveLearning(nw.profile.name)
        context  = nw.snapshot_context(wifi)
        telemetry_session = _setup_telemetry(nw, context, telemetry)

        start_time = time.perf_counter()
        attempts   = 0
        bias       = learning.get_bias()

        # Intervalo base de polling — aqui smart=True porque é o intervalo
        # interno do polling, não um tempo de espera garantido ao usuário
        base_interval = nw.compute_wait(nw.profile.poll_interval, speed_value, context, smart=True)
        base_interval = max(0.01, min(0.3, base_interval))

        while (time.perf_counter() - start_time) < timeout:
            try:
                if t():
                    telemetry_session.stop()
                    learning.update(True, 1.0, 1.0)
                    return True
            except Exception as e:
                if verbose:
                    print(f"[NanoWait] Condition error (attempt {attempts}): {e}")

            # Backoff suave: cresce até 2x no máximo, com teto de 0.5s
            elapsed_ratio = min(1.0, (time.perf_counter() - start_time) / max(timeout, 1))
            interval = base_interval * (1 + elapsed_ratio) * bias
            interval = round(max(0.01, min(0.5, interval)), 4)

            if telemetry:
                telemetry_session.record(factor=speed_value, interval=interval)
            if verbose:
                print(f"[NanoWait | {nw.profile.name}] Polling #{attempts}: interval={interval:.3f}s")
            if log:
                from .utils import log_message
                log_message(f"[NanoWait | {nw.profile.name}] Poll #{attempts}: {interval:.3f}s")

            time.sleep(interval)
            attempts += 1

        telemetry_session.stop()
        learning.update(False, 1.0, 1.0)

        if raise_on_timeout:
            raise WaitTimeoutError(
                f"Condition not met after {timeout}s ({attempts} attempts)."
            )
        return False

    # ── MODO TEMPO (FLOAT ou None) ────────────────────────────────────
    if t is not None and not isinstance(t, (int, float)):
        raise TypeError(f"wait() expects float, callable or None — got {type(t).__name__}")

    learning  = AdaptiveLearning(nw.profile.name)
    context   = nw.snapshot_context(wifi)
    telemetry_session = _setup_telemetry(nw, context, telemetry)

    base_t        = float(t) if t is not None else 1.0

    # Passa smart para compute_wait:
    # - smart=False → nunca entrega menos do que base_t
    # - smart=True  → pode reduzir em sistemas ociosos
    adaptive_wait = nw.compute_wait(base_t, speed_value, context, smart=smart)
    adaptive_wait = max(0.005, adaptive_wait)

    bias       = learning.get_bias()
    final_wait = round(max(0.005, adaptive_wait * bias), 4)

    if telemetry:
        telemetry_session.record(factor=speed_value, interval=final_wait)
    if verbose:
        mode_label = "smart" if smart else "normal"
        print(
            f"[NanoWait | {nw.profile.name} | {mode_label}] "
            f"requested={base_t}s → final={final_wait}s "
            f"(speed={speed_value:.2f}, bias={bias:.3f})"
        )
    if log:
        from .utils import log_message
        log_message(
            f"[NanoWait | {nw.profile.name}] "
            f"requested={base_t}s → final={final_wait}s"
        )

    try:
        time.sleep(final_wait)
        learning.update(True, base_t, final_wait)
    except Exception:
        learning.update(False, base_t, final_wait)
        raise
    finally:
        telemetry_session.stop()

    if explain:
        return ExplainReport(
            requested_time=t,
            final_time=final_wait,
            speed_input=speed,
            speed_value=speed_value,
            smart=smart,
            cpu_score=context["pc_score"],
            wifi_score=context["wifi_score"],
            factor=speed_value,
            min_floor_applied=final_wait <= 0.005,
            max_cap_applied=not smart and t is not None and final_wait >= float(t),
            timestamp=datetime.utcnow().isoformat(),
        )

    return final_wait

# ──────────────────────────────────────────────
# Funções Utilitárias Adicionais
# ──────────────────────────────────────────────

def wait_until(
    condition: Callable[[], bool],
    *,
    timeout:   float = 15.0,
    msg:       str = "Condition not met within timeout.",
    **kwargs,
) -> bool:
    """
    Versão semântica de wait() para condições.
    Lança WaitTimeoutError com mensagem customizável em caso de timeout.

    Exemplo:
        wait_until(lambda: page.is_loaded(), timeout=10, msg="Page not loaded")

    Args:
        condition: Callable que retorna True quando a condição é satisfeita.
        timeout:   Tempo máximo de espera em segundos.
        msg:       Mensagem de erro em caso de timeout.
        **kwargs:  Demais opções de wait() (speed, smart, profile, etc.).

    Raises:
        WaitTimeoutError: Se a condição não for satisfeita dentro do timeout.
    """
    result = wait(condition, timeout=timeout, raise_on_timeout=False, **kwargs)
    if not result:
        raise WaitTimeoutError(msg)
    return True


@contextmanager
def timed_wait(label: str = "block", verbose: bool = True):
    """
    Context manager para medir o tempo de execução de um bloco de código.

    Exemplo:
        with timed_wait("login") as info:
            driver.find_element(...).click()
        print(f"Login levou {info['duration']:.3f}s")

    Yields:
        dict com 'label' e 'duration' (preenchido ao sair do bloco).
    """
    info = {"label": label, "duration": 0.0}
    start = time.perf_counter()
    try:
        yield info
    finally:
        info["duration"] = round(time.perf_counter() - start, 4)
        if verbose:
            print(f"[NanoWait | timed_wait] {label}: {info['duration']:.4f}s")