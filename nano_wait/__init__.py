# nano_wait/__init__.py
__version__ = "5.0.2"  # ou qualquer versão que você queira testar

from .nano_wait import wait, NanoWait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool, wait_pool_async
from .nano_wait_auto import wait_auto

__all__ = [
    "wait",
    "wait_auto",
    "NanoWait",
    "wait_async",
    "wait_pool",
    "wait_pool_async",
]
