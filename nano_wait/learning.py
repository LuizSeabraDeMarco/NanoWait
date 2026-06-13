"""
NanoWait Adaptive Learning
--------------------------
Persiste um bias por perfil em ~/.nano_wait_learning.json
e atualiza via EMA (Exponential Moving Average).

Melhorias v7:
- Gravação com debounce: só escreve no disco a cada N updates ou ao fechar
- Cache de classe com invalidação correta
- Sem I/O desnecessário em cada update
"""

import json
import os
import threading
import atexit
from pathlib import Path
from typing import Dict, Any, Optional


class AdaptiveLearning:
    _lock       = threading.Lock()
    _storage    = Path.home() / ".nano_wait_learning.json"
    _data: Optional[Dict[str, Any]] = None   # cache compartilhado
    _dirty      = False                       # indica que há dados não salvos
    _write_every = 5                          # salva a cada N updates

    # Registra flush ao fechar o processo
    _atexit_registered = False

    def __init__(self, profile: str):
        self.profile = profile
        self.alpha   = 0.1  # EMA smoothing factor

        with AdaptiveLearning._lock:
            if AdaptiveLearning._data is None:
                AdaptiveLearning._data = self._load()

            if profile not in AdaptiveLearning._data["profiles"]:
                AdaptiveLearning._data["profiles"][profile] = {
                    "bias":     1.0,
                    "samples":  0,
                    "timeouts": 0,
                }
                self._flush()

            # Registra o atexit apenas uma vez
            if not AdaptiveLearning._atexit_registered:
                atexit.register(AdaptiveLearning._flush_static)
                AdaptiveLearning._atexit_registered = True

    # ──────────────────────────────────────────
    # Persistência
    # ──────────────────────────────────────────

    def _load(self) -> Dict[str, Any]:
        if not self._storage.exists():
            return {"profiles": {}, "_meta": {"version": 7}}
        try:
            with open(self._storage, "r") as f:
                data = json.load(f)
            # Compatibilidade com versões anteriores
            if "profiles" not in data:
                data = {"profiles": {}, "_meta": {"version": 7}}
            return data
        except Exception:
            return {"profiles": {}, "_meta": {"version": 7}}

    def _flush(self):
        """Salva em disco (deve ser chamado dentro do _lock)."""
        try:
            with open(self._storage, "w") as f:
                json.dump(AdaptiveLearning._data, f, indent=2)
            AdaptiveLearning._dirty = False
        except Exception:
            pass  # Não quebramos o fluxo por falha de I/O

    @staticmethod
    def _flush_static():
        """Chamado pelo atexit para garantir flush final."""
        with AdaptiveLearning._lock:
            if AdaptiveLearning._dirty and AdaptiveLearning._data is not None:
                try:
                    path = Path.home() / ".nano_wait_learning.json"
                    with open(path, "w") as f:
                        json.dump(AdaptiveLearning._data, f, indent=2)
                except Exception:
                    pass

    # ──────────────────────────────────────────
    # API Pública
    # ──────────────────────────────────────────

    def get_bias(self) -> float:
        """Retorna o bias atual para o perfil (thread-safe, sem I/O)."""
        with AdaptiveLearning._lock:
            return AdaptiveLearning._data["profiles"][self.profile]["bias"]

    def update(self, success: bool, expected: float, actual: float):
        """
        Atualiza o bias via EMA baseado na razão actual/expected.

        Gravação em disco é deferred (debounce a cada _write_every updates).
        """
        with AdaptiveLearning._lock:
            pdata = AdaptiveLearning._data["profiles"][self.profile]
            pdata["samples"] += 1

            if not success:
                pdata["timeouts"] += 1

            ratio = (actual / expected) if expected > 0 else 1.0

            old_bias = pdata["bias"]
            new_bias = old_bias * (1 - self.alpha) + ratio * self.alpha

            # Penaliza levemente em caso de timeout
            if not success:
                new_bias *= 1.05

            new_bias = max(0.5, min(2.5, new_bias))
            pdata["bias"] = round(new_bias, 4)

            AdaptiveLearning._dirty = True

            # Debounce: salva apenas a cada N samples
            if pdata["samples"] % AdaptiveLearning._write_every == 0:
                self._flush()

    def reset(self):
        """Reseta o bias do perfil para 1.0 (neutro)."""
        with AdaptiveLearning._lock:
            AdaptiveLearning._data["profiles"][self.profile] = {
                "bias":     1.0,
                "samples":  0,
                "timeouts": 0,
            }
            self._flush()

    def stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do perfil atual."""
        with AdaptiveLearning._lock:
            pdata = AdaptiveLearning._data["profiles"][self.profile]
            s = pdata["samples"]
            t = pdata["timeouts"]
            return {
                "profile":       self.profile,
                "bias":          pdata["bias"],
                "samples":       s,
                "timeouts":      t,
                "success_rate":  round((s - t) / s, 4) if s > 0 else 1.0,
            }

    @classmethod
    def all_profiles_stats(cls) -> Dict[str, Any]:
        """Retorna estatísticas de todos os perfis aprendidos."""
        with cls._lock:
            if cls._data is None:
                return {}
            return {
                name: {
                    "bias":         p["bias"],
                    "samples":      p["samples"],
                    "success_rate": round(
                        (p["samples"] - p["timeouts"]) / p["samples"], 4
                    ) if p["samples"] > 0 else 1.0,
                }
                for name, p in cls._data["profiles"].items()
            }
