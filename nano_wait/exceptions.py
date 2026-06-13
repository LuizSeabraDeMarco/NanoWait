"""
NanoWait Exceptions
-------------------
Exceções customizadas da biblioteca.
"""


class WaitTimeoutError(TimeoutError):
    """
    Lançada quando uma condição callable não se torna True dentro do timeout.

    Herda de TimeoutError para compatibilidade com código que capture
    erros genéricos de timeout.
    """


class VisionTimeout(Exception):
    """
    Lançada quando uma condição visual não é detectada dentro do timeout.
    Usada pelo módulo de visão computacional (vision.py).
    """


class InvalidProfileError(ValueError):
    """
    Lançada quando um perfil de execução inválido é especificado.
    """
    def __init__(self, profile: str, available: list):
        super().__init__(
            f"Profile '{profile}' não existe. "
            f"Disponíveis: {', '.join(available)}"
        )
        self.profile   = profile
        self.available = available


class SpeedValueError(ValueError):
    """
    Lançada quando um preset de velocidade inválido é fornecido.
    """
