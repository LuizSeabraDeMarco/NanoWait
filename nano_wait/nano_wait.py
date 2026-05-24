"""
NanoWait Main API
-----------------
Interface de alto nível para o motor de execução adaptativo.
Oferece suporte a esperas baseadas em tempo, condições e telemetria.
"""

import time
import queue
import socket
from typing import overload, Callable, Optional, Union, Dict, Any
from datetime import datetime

from .learning import AdaptiveLearning
from .core import NanoWait, PROFILES
from .utils import get_speed_value
from .explain import ExplainReport
from .telemetry import TelemetrySession
from .dashboard import TelemetryDashboard

_ENGINE = None

def _get_engine(profile: Optional[str] = None) -> NanoWait:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = NanoWait(profile)
    elif profile and _ENGINE.profile.name != profile:
        _ENGINE.profile = PROFILES.get(profile, PROFILES["default"])
    return _ENGINE

def has_internet(host="8.8.8.8", port=53, timeout=1) -> bool:
    """Verifica conectividade básica de rede."""
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except Exception:
        return False

def _setup_telemetry(nw: NanoWait, context: Dict[str, Any], enabled: bool):
    """Configura sessão de telemetria se habilitado."""
    telemetry_queue = queue.Queue() if enabled else None
    if enabled:
        try:
            TelemetryDashboard(telemetry_queue).start()
        except Exception:
            pass

    session = TelemetrySession(
        enabled=enabled,
        cpu_score=context["pc_score"],
        wifi_score=context["wifi_score"],
        profile=nw.profile.name,
        queue=telemetry_queue
    )
    session.start()
    return session

@overload
def wait(t: float, **kwargs) -> float: ...

@overload
def wait(until: Callable, **kwargs) -> bool: ...

def wait(
    t: Union[float, Callable, None] = None,
    *,
    timeout: float = 15.0,
    wifi: Optional[str] = None,
    speed: Union[str, float] = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False,
    explain: bool = False,
    telemetry: bool = False,
    profile: Optional[str] = None
) -> Union[float, bool, ExplainReport]:
    """
    Executa uma espera adaptativa baseada em tempo ou condição.
    """
    nw = _get_engine(profile)
    verbose = verbose or nw.profile.verbose
    
    # Resolução de velocidade (fator global para a chamada)
    speed_value = nw.smart_speed(wifi) if smart else get_speed_value(speed)

    # --- MODO CONDIÇÃO (CALLABLE) ---
    if callable(t):
        if timeout <= 0: return False
        
        # MUDANÇA: Movido para fora do loop para evitar overhead repetitivo
        learning = AdaptiveLearning(nw.profile.name)
        context = nw.snapshot_context(wifi)
        telemetry_session = _setup_telemetry(nw, context, telemetry)
        
        start_time = time.time()
        attempts = 0
        
        # MUDANÇA: Cache de bias para evitar I/O de leitura no loop
        bias = learning.get_bias()
        
        while (time.time() - start_time) < timeout:
            try:
                if t():
                    telemetry_session.stop()
                    learning.update(True, 1.0, 1.0)
                    return True
            except Exception as e:
                if verbose: print(f"[NanoWait] Condition Error: {e}")
            
            # Cálculo de intervalo adaptativo para polling
            interval = nw.compute_wait(0.1, speed_value, context)
            
            # MUDANÇA: Piso reduzido de 0.05s para 0.02s para maior agilidade
            interval = max(0.02, min(0.5, interval)) 
            
            interval = round(interval * bias, 4)
            
            if telemetry:
                telemetry_session.record(factor=speed_value, interval=interval)
            
            if verbose:
                print(f"[NanoWait | {nw.profile.name}] Polling: {interval:.3f}s | Attempt: {attempts}")
            
            time.sleep(interval)
            attempts += 1
            
        telemetry_session.stop()
        learning.update(False, 1.0, 1.0)
        return False

    # --- MODO TEMPO (FLOAT) ---
    if t is not None and not isinstance(t, (int, float)):
        raise TypeError("wait() requires float, callable, or None")

    # MUDANÇA: Inicialização movida para garantir snapshot único por chamada
    learning = AdaptiveLearning(nw.profile.name)
    context = nw.snapshot_context(wifi)
    telemetry_session = _setup_telemetry(nw, context, telemetry)

    base_t = float(t) if t is not None else 1.0
    adaptive_wait = nw.compute_wait(base_t, speed_value, context)
    
    if not smart and t is not None:
        adaptive_wait = min(adaptive_wait, t)
    
    adaptive_wait = round(max(0.01, adaptive_wait), 4)
    bias = learning.get_bias()
    final_wait = round(adaptive_wait * bias, 4)

    if telemetry:
        telemetry_session.record(factor=speed_value, interval=final_wait)
    
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
            min_floor_applied=final_wait <= 0.01,
            max_cap_applied=not smart and t is not None and final_wait >= t,
            timestamp=datetime.utcnow().isoformat()
        )

    return final_wait
