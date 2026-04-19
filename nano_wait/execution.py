"""
NanoWait Execution Engine
-------------------------
O motor de execução orquestra a execução de funções com lógica de retentativa 
e adaptabilidade. Ele garante que uma operação seja concluída com sucesso 
ou expire conforme o timeout, ajustando o intervalo de polling dinamicamente.
"""

import time
from dataclasses import dataclass
from typing import Callable, Any, Optional, TypeVar, Generic

from .nano_wait import wait

T = TypeVar('T')

@dataclass
class ExecutionResult(Generic[T]):
    """Resultado imutável de uma operação executada pelo NanoWait."""
    success: bool
    result: Optional[T]
    attempts: int
    duration: float
    error: Optional[Exception] = None

    def __repr__(self) -> str:
        status = "✅ SUCCESS" if self.success else "❌ FAILURE"
        return f"ExecutionResult({status}, attempts={self.attempts}, duration={self.duration:.3f}s)"

def execute(
    fn: Callable[[], T],
    *,
    timeout: float = 10.0,
    interval: float = 0.2,
    profile: Optional[str] = None,
    verbose: bool = False,
    smart: bool = True
) -> ExecutionResult[T]:
    """
    Executa repetidamente uma função até que ela retorne um valor verdadeiro ou o tempo expire.
    
    :param fn: Função a ser executada (deve retornar um valor avaliado como True no sucesso).
    :param timeout: Tempo máximo total para tentativas em segundos.
    :param interval: Intervalo base entre tentativas (ajustado pelo motor se smart=True).
    :param profile: Perfil de execução ("ci", "testing", "rpa").
    :param verbose: Ativa logs detalhados durante a execução.
    :param smart: Habilita adaptabilidade do intervalo baseada em hardware.
    """
    start_time = time.time()
    attempts = 0
    last_error = None

    while (time.time() - start_time) < timeout:
        try:
            result = fn()
            
            # Se a função retornar algo que avalie como verdadeiro, consideramos sucesso
            if result:
                return ExecutionResult(
                    success=True,
                    result=result,
                    attempts=attempts + 1,
                    duration=round(time.time() - start_time, 4)
                )
                
        except Exception as e:
            last_error = e
            if verbose:
                print(f"[NanoWait Execution] Attempt {attempts + 1} failed: {e}")

        # Delegamos a espera ao motor central, que ajusta o intervalo
        # conforme o contexto do sistema e o perfil escolhido.
        wait(
            interval, 
            profile=profile, 
            smart=smart, 
            verbose=verbose
        )
        attempts += 1

    return ExecutionResult(
        success=False,
        result=None,
        attempts=attempts,
        duration=round(time.time() - start_time, 4),
        error=last_error
    )
