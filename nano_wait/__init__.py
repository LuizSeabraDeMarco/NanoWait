"""
🚀 NanoWait — Adaptive Execution Engine for Python
-------------------------------------------------
Uma biblioteca para automação inteligente que substitui o time.sleep() estático 
por um motor de execução adaptativo baseado em telemetria de hardware e rede.
"""

__version__ = "6.0.0"
__author__ = "NanoWait Team"

from .nano_wait import wait, NanoWait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool, wait_pool_async
from .nano_wait_auto import wait_auto

# Camada de Execução e Retentativa
from .execution import execute, ExecutionResult
from .decorators import retry

# Camada de Agente (Experimental)
try:
    from .agent import Agent
except ImportError:
    Agent = None

__all__ = [
    "wait",
    "wait_auto",
    "NanoWait",
    "wait_async",
    "wait_pool",
    "wait_pool_async",
    "execute",
    "ExecutionResult",
    "retry",
    "Agent",
]
