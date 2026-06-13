"""
NanoWait Utils
--------------
Utilitários internos compartilhados.
"""

import os
from datetime import datetime
from typing import Union

# Mapeamento de presets de velocidade para float
SPEED_MAP = {
    "crawl":  0.3,   # muito lento, máxima estabilidade
    "slow":   0.8,
    "normal": 1.5,
    "fast":   3.0,
    "ultra":  6.0,
    "turbo":  10.0,  # máxima velocidade possível
}

# Tamanho máximo do log antes de rotacionar (100 KB)
_MAX_LOG_BYTES = 100 * 1024


def get_speed_value(speed: Union[str, float]) -> float:
    """
    Converte preset de velocidade ou valor numérico para float.

    Presets disponíveis: "crawl", "slow", "normal", "fast", "ultra", "turbo"

    Args:
        speed: Nome do preset ou valor float diretamente.

    Returns:
        float representando o fator de velocidade.
    """
    if isinstance(speed, str):
        key = speed.strip().lower()
        if key not in SPEED_MAP:
            raise ValueError(
                f"Speed preset '{speed}' inválido. "
                f"Opções: {', '.join(SPEED_MAP)}"
            )
        return SPEED_MAP[key]
    return float(speed)


def log_message(text: str, path: str = "nano_wait.log"):
    """
    Salva mensagem em arquivo de log com rotação automática.

    Se o arquivo ultrapassar 100 KB, é renomeado para .log.bak
    e um novo arquivo é criado.

    Args:
        text: Mensagem a registrar.
        path: Caminho do arquivo de log (padrão: nano_wait.log).
    """
    # Rotação automática
    if os.path.exists(path) and os.path.getsize(path) > _MAX_LOG_BYTES:
        bak = path + ".bak"
        try:
            if os.path.exists(bak):
                os.remove(bak)
            os.rename(path, bak)
        except OSError:
            pass

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {text}\n")
    except OSError:
        pass  # Não quebramos o fluxo por falha de I/O
