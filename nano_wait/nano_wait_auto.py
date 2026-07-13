
import time
from typing import Optional, Union
 
from .learning import AdaptiveLearning
from .core import NanoWait
from .telemetry import TelemetrySession
from .utils import log_message
from .nano_wait import has_internet, _get_engine
 
 
def wait_auto(
    t:         Optional[float] = None,
    *,
    wifi:      Optional[str] = None,
    profile:   Optional[str] = None,
    verbose:   bool = False,
    log:       bool = False,
    telemetry: bool = False,
    explain:   bool = False,
) -> Union[float, dict]:
    """
    Espera totalmente automática: detecta condições do sistema e rede
    e escolhe o melhor intervalo sem configuração manual.
 
    Args:
        t:         Tempo máximo de espera (None = totalmente automático).
        wifi:      SSID da rede para medir sinal.
        profile:   Perfil de execução.
        verbose:   Logs detalhados.
        log:       Salva em nano_wait.log.
        telemetry: Ativa telemetria.
        explain:   Retorna dict com detalhes.
 
    Returns:
        float: Tempo de espera real.
        dict:  Detalhes (quando explain=True).
    """
    # Engine dedicado ao perfil — sem mutação de estado compartilhado.
    nw: NanoWait = _get_engine(profile)
 
    learning = AdaptiveLearning(nw.profile.name)
    verbose  = verbose or nw.profile.verbose
    context  = nw.snapshot_context(wifi)
 
    cpu_score  = context["pc_score"]
    wifi_score = context["wifi_score"]
 
    telemetry_session = TelemetrySession(
        enabled=telemetry,
        cpu_score=cpu_score,
        wifi_score=wifi_score,
        profile=nw.profile.name,
    )
    telemetry_session.start()
 
    speed_value = nw.smart_speed(wifi)
 
    # Escolhe estratégia baseado em conectividade
    if wifi or has_internet():
        factor = nw.compute_wait_wifi(speed_value, wifi, context=context)
    else:
        factor = nw.compute_wait_no_wifi(speed_value, context=context)
 
    # Converte fator em intervalo
    interval = max(0.005, 1 / max(factor, 0.01))
    interval = nw.apply_profile(interval)
 
    if t is not None:
        interval = min(interval, float(t))
 
    bias     = learning.get_bias()
    interval = round(max(0.005, interval * bias), 4)
 
    telemetry_session.record(factor=factor, interval=interval)
 
    if verbose:
        print(
            f"[NanoWait AUTO | {nw.profile.name}] "
            f"factor={factor:.2f} bias={bias:.3f} wait={interval:.4f}s"
        )
    if log:
        log_message(
            f"[NanoWait AUTO | {nw.profile.name}] "
            f"factor={factor:.2f} bias={bias:.3f} wait={interval:.4f}s"
        )
 
    try:
        time.sleep(interval)
        learning.update(True, interval, interval)
    except Exception:
        learning.update(False, interval, interval)
        raise
    finally:
        telemetry_session.stop()
 
    if explain:
        return {
            "interval":   interval,
            "factor":     factor,
            "cpu_score":  cpu_score,
            "wifi_score": wifi_score,
            "profile":    nw.profile.name,
            "bias":       bias,
        }
 
    return interval
 