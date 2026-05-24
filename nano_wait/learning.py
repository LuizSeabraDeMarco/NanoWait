import json
import os
import threading
from pathlib import Path

class AdaptiveLearning:
    _lock = threading.Lock()
    _storage_path = Path.home() / ".nano_wait_learning.json"
    # MUDANÇA: Adicionado cache de dados para evitar I/O repetitivo
    _cached_data = None

    def __init__(self, profile: str):
        self.profile = profile
        self.alpha = 0.1  # EMA smoothing factor
        
        # MUDANÇA: Carrega do disco apenas se o cache estiver vazio
        if AdaptiveLearning._cached_data is None:
            AdaptiveLearning._cached_data = self._load()
        self._data = AdaptiveLearning._cached_data

        if profile not in self._data["profiles"]:
            self._data["profiles"][profile] = {
                "bias": 1.0,
                "samples": 0,
                "timeouts": 0
            }
            self._save()

    # --------------------------
    # Persistence
    # --------------------------

    def _load(self):
        if not self._storage_path.exists():
            return {
                "profiles": {}
            }

        try:
            with open(self._storage_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"profiles": {}}

    def _save(self):
        with self._lock:
            with open(self._storage_path, "w") as f:
                json.dump(self._data, f, indent=2)

    # --------------------------
    # Public API
    # --------------------------

    def get_bias(self) -> float:
        return self._data["profiles"][self.profile]["bias"]

    def update(self, success: bool, expected: float, actual: float):
        profile_data = self._data["profiles"][self.profile]

        profile_data["samples"] += 1

        if not success:
            profile_data["timeouts"] += 1

        # EMA update based on performance ratio
        if expected > 0:
            ratio = actual / expected
        else:
            ratio = 1.0

        old_bias = profile_data["bias"]
        new_bias = old_bias * (1 - self.alpha) + ratio * self.alpha

        # Penaliza levemente se houve timeout
        if not success:
            new_bias *= 1.05

        # Limites de segurança
        new_bias = max(0.5, min(2.5, new_bias))

        profile_data["bias"] = round(new_bias, 4)

        self._save()
