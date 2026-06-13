"""
🚀 NanoWait — Adaptive Execution Engine for Python
--------------------------------------------------
Uma biblioteca que substitui time.sleep() estático por um motor de execução
adaptativo baseado em telemetria de hardware e aprendizado contínuo.

Uso rápido:
    from nano_wait import wait

    wait(2)                              # espera adaptativa de ~2s
    wait(lambda: btn.visible(), timeout=10)  # polling inteligente
    wait(2, smart=True)                  # velocidade autodetectada
    wait_until(lambda: x > 0, msg="x nunca ficou positivo")
"""

__version__ = "7.0.0"
__author__  = "NanoWait Team"

# API principal
from .nano_wait import wait, wait_until, timed_wait, has_internet
from .core import NanoWait, PROFILES, ExecutionProfile

# Async
from .nano_wait_async import wait_async

# Pool
from .nano_wait_pool import wait_pool, wait_pool_async

# Auto
from .nano_wait_auto import wait_auto

# Execução e Retry
from .execution import execute, ExecutionResult

# Decorators
from .decorators import retry, timed, wait_before

# Aprendizado
from .learning import AdaptiveLearning

# Exceções
from .exceptions import WaitTimeoutError, VisionTimeout, InvalidProfileError

# Agente experimental
try:
    from .agent import Agent
except ImportError:
    Agent = None  # type: ignore

__all__ = [
    # Core API
    "wait",
    "wait_until",
    "timed_wait",
    "has_internet",
    "NanoWait",
    "PROFILES",
    "ExecutionProfile",

    # Async
    "wait_async",

    # Pool
    "wait_pool",
    "wait_pool_async",

    # Auto
    "wait_auto",

    # Execution
    "execute",
    "ExecutionResult",

    # Decorators
    "retry",
    "timed",
    "wait_before",

    # Learning
    "AdaptiveLearning",

    # Exceptions
    "WaitTimeoutError",
    "VisionTimeout",
    "InvalidProfileError",

    # Experimental
    "Agent",
]
