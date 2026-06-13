"""
NanoWait Execution Engine
--------------------------
Orquestra execução de funções com lógica de retentativa e adaptabilidade.

Melhorias v7:
- Parâmetro max_attempts para limitar tentativas independente do timeout
- Callback on_error chamado a cada falha
- Suporte a exceções esperadas (expected_exceptions)
- ExecutionResult.raise_if_failed() para integração fluente
"""

import time
from dataclasses import dataclass, field
from typing import Callable, Any, Optional, TypeVar, Generic, Type, Tuple

from .nano_wait import wait

T = TypeVar("T")


@dataclass
class ExecutionResult(Generic[T]):
    """Resultado imutável de uma operação executada pelo NanoWait."""
    success:   bool
    result:    Optional[T]
    attempts:  int
    duration:  float
    error:     Optional[Exception] = field(default=None, repr=False)

    def __repr__(self) -> str:
        status = "✅ SUCCESS" if self.success else "❌ FAILURE"
        return (
            f"ExecutionResult({status}, "
            f"attempts={self.attempts}, "
            f"duration={self.duration:.3f}s)"
        )

    def raise_if_failed(self) -> "ExecutionResult[T]":
        """
        Lança a última exceção se a execução falhou.
        Conveniente para pipelines fluentes.

        Exemplo:
            result = execute(my_fn, timeout=5).raise_if_failed()
        """
        if not self.success and self.error is not None:
            raise self.error
        elif not self.success:
            from .exceptions import WaitTimeoutError
            raise WaitTimeoutError(
                f"Execution failed after {self.attempts} attempts "
                f"in {self.duration:.3f}s."
            )
        return self


def execute(
    fn: Callable[[], T],
    *,
    timeout:              float = 10.0,
    interval:             float = 0.2,
    max_attempts:         Optional[int] = None,
    profile:              Optional[str] = None,
    verbose:              bool = False,
    smart:                bool = True,
    on_error:             Optional[Callable[[Exception, int], None]] = None,
    expected_exceptions:  Tuple[Type[Exception], ...] = (Exception,),
) -> ExecutionResult[T]:
    """
    Executa uma função repetidamente até sucesso ou expiração do timeout.

    Args:
        fn:                   Função a executar (retorno truthy = sucesso).
        timeout:              Tempo máximo total em segundos.
        interval:             Intervalo base entre tentativas.
        max_attempts:         Limite máximo de tentativas (independente do timeout).
        profile:              Perfil NanoWait ("ci", "testing", "rpa", "turbo", "safe").
        verbose:              Logs detalhados.
        smart:                Ajusta interval pelo hardware.
        on_error:             Callback(exception, attempt_number) chamado a cada falha.
        expected_exceptions:  Exceções capturáveis (padrão: todas).

    Returns:
        ExecutionResult com success, result, attempts, duration e error.

    Exemplo:
        result = execute(
            lambda: api.fetch_user(id=42),
            timeout=10,
            on_error=lambda e, n: print(f"Retry {n}: {e}"),
        )
        if result.success:
            print(result.result)
    """
    start_time = time.perf_counter()
    attempts   = 0
    last_error: Optional[Exception] = None

    while (time.perf_counter() - start_time) < timeout:
        if max_attempts is not None and attempts >= max_attempts:
            break

        try:
            result = fn()
            if result or result == 0:  # 0 é um resultado válido
                return ExecutionResult(
                    success=True,
                    result=result,
                    attempts=attempts + 1,
                    duration=round(time.perf_counter() - start_time, 4),
                )
        except expected_exceptions as e:
            last_error = e
            if verbose:
                print(f"[NanoWait Execute] Attempt {attempts + 1} failed: {e}")
            if on_error is not None:
                try:
                    on_error(e, attempts + 1)
                except Exception:
                    pass

        wait(interval, profile=profile, smart=smart, verbose=False)
        attempts += 1

    return ExecutionResult(
        success=False,
        result=None,
        attempts=attempts,
        duration=round(time.perf_counter() - start_time, 4),
        error=last_error,
    )
