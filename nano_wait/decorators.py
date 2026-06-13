"""
NanoWait Decorators
-------------------
Decorators powered by NanoWait execution engine.

Melhorias v7:
- @retry: suporte a max_attempts, on_error e expected_exceptions
- @timed: mede e imprime o tempo de execução de uma função
- @wait_before: aplica wait() adaptativo antes de cada chamada
"""

import time
from functools import wraps
from typing import Callable, Optional, Tuple, Type

from .execution import execute


def retry(
    timeout:             float = 5.0,
    interval:            float = 0.2,
    max_attempts:        Optional[int] = None,
    profile:             Optional[str] = None,
    smart:               bool = True,
    verbose:             bool = False,
    expected_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_error:            Optional[Callable] = None,
):
    """
    Retry decorator powered by NanoWait execution engine.

    Executa a função decorada repetidamente até obter um retorno truthy
    ou expirar o timeout.

    Args:
        timeout:             Tempo máximo em segundos.
        interval:            Intervalo base entre tentativas.
        max_attempts:        Limite máximo de tentativas.
        profile:             Perfil NanoWait.
        smart:               Ajusta interval pelo hardware.
        verbose:             Logs detalhados.
        expected_exceptions: Exceções a capturar (padrão: todas).
        on_error:            Callback(exc, attempt) chamado a cada falha.

    Exemplo:
        @retry(timeout=10, max_attempts=5)
        def fetch_data():
            return requests.get(url).json()
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return execute(
                lambda: fn(*args, **kwargs),
                timeout=timeout,
                interval=interval,
                max_attempts=max_attempts,
                profile=profile,
                smart=smart,
                verbose=verbose,
                expected_exceptions=expected_exceptions,
                on_error=on_error,
            )
        return wrapper
    return decorator


def timed(label: Optional[str] = None, verbose: bool = True):
    """
    Mede e imprime o tempo de execução de uma função.

    Args:
        label:   Nome a exibir (padrão: nome da função).
        verbose: Se False, suprime o print (mas ainda retorna o resultado).

    Exemplo:
        @timed()
        def load_page():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            name  = label or fn.__qualname__
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed = round(time.perf_counter() - start, 4)
            if verbose:
                print(f"[NanoWait | timed] {name}: {elapsed:.4f}s")
            return result
        return wrapper
    return decorator


def wait_before(
    seconds: float = 1.0,
    *,
    speed:   str = "normal",
    smart:   bool = False,
    profile: Optional[str] = None,
):
    """
    Aplica uma espera adaptativa antes de cada chamada da função decorada.

    Útil para automações que precisam de um delay antes de interagir
    com elementos de UI.

    Args:
        seconds: Tempo base de espera.
        speed:   Fator de velocidade.
        smart:   Auto-detecta velocidade pelo hardware.
        profile: Perfil NanoWait.

    Exemplo:
        @wait_before(0.5, smart=True)
        def click_button(driver, selector):
            driver.find_element(selector).click()
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from .nano_wait import wait
            wait(seconds, speed=speed, smart=smart, profile=profile)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
