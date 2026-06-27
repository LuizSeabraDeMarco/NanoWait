"""
NanoWait Core Engine
--------------------
Base teórica: O NanoWait opera sob o princípio de "Observabilidade de Execução".
Diferente de um sleep estático, ele utiliza telemetria em tempo real (CPU, Memória, Rede)
para calcular o "Custo de Oportunidade de Espera".

Fórmula base (modo smart=True):
    WaitTime = (BaseTime / (SystemHealth * SpeedFactor)) * ProfileAggressiveness

Fórmula base (modo padrão, smart=False):
    WaitTime = BaseTime * (1 + overload_penalty) * ProfileAggressiveness
    — nunca entrega menos tempo do que o solicitado

SystemHealth ∈ [0, 10]  — derivado de CPU + RAM
SpeedFactor  ∈ [0.5, 6] — controlado pelo usuário ou autodetectado
"""

import platform
import time
import subprocess
from dataclasses import dataclass
from typing import Optional, Dict, Any

# ──────────────────────────────────────────────
# Perfis de Execução
# ──────────────────────────────────────────────

@dataclass(frozen=True)
class ExecutionProfile:
    """Define comportamento de agressividade e tolerância do motor."""
    name: str
    aggressiveness: float  # Multiplicador para intervalos (menor = mais rápido)
    tolerance: float       # Permissividade a falhas temporárias [0.0, 1.0]
    poll_interval: float   # Base para loops de polling em segundos
    verbose: bool          # Ativa logs detalhados por padrão

PROFILES: Dict[str, ExecutionProfile] = {
    "ci":       ExecutionProfile("ci",       0.4, 0.9, 0.03, True),
    "testing":  ExecutionProfile("testing",  0.8, 0.7, 0.08, True),
    "rpa":      ExecutionProfile("rpa",      2.0, 0.5, 0.2,  False),
    "default":  ExecutionProfile("default",  1.0, 0.8, 0.1,  False),
    "turbo":    ExecutionProfile("turbo",    0.25, 0.95, 0.01, False),
    "safe":     ExecutionProfile("safe",     3.0, 0.3, 0.5,  False),
}

# ──────────────────────────────────────────────
# Motor Central
# ──────────────────────────────────────────────

class NanoWait:
    """
    Motor central que orquestra coleta de contexto e ajuste de timing.

    Comportamento padrão (smart=False):
    - wait(2) NUNCA entrega menos de 2s — só pode aumentar se o sistema estiver lento.
    - Isso garante previsibilidade para testes e automação.

    Comportamento smart (smart=True):
    - Pode reduzir o tempo em sistemas ociosos e rápidos.
    - Útil quando a espera é apenas uma "cortesia" ao sistema, não um requisito.
    """

    CONTEXT_TTL = 2.0

    def __init__(self, profile: Optional[str] = None):
        self.system = platform.system().lower()
        self.profile = PROFILES.get(profile, PROFILES["default"])
        self._wifi_interface = None
        self._initialized_wifi = False

        self._ctx_cache: Optional[Dict[str, Any]] = None
        self._ctx_ts: float = 0.0

        try:
            import psutil
            psutil.cpu_percent(interval=0.1)
        except Exception:
            pass

    # ──────────────────────────────────────────
    # Wi-Fi (lazy init)
    # ──────────────────────────────────────────

    def _init_wifi(self):
        """Lazy initialization para evitar overhead se não for usado."""
        if self._initialized_wifi:
            return
        if self.system == "windows":
            try:
                import pywifi
                wifi = pywifi.PyWiFi()
                self._wifi_interface = wifi.interfaces()[0]
            except Exception:
                self._wifi_interface = None
        self._initialized_wifi = True

    # ──────────────────────────────────────────
    # Coleta de Métricas
    # ──────────────────────────────────────────

    def get_pc_score(self) -> float:
        """
        Score de performance do sistema [0, 10].
        10 = sistema ocioso e rápido; 0 = sistema sob estresse extremo.
        """
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent

            cpu_penalty = cpu / 10 + max(0, (cpu - 80) / 20)
            mem_penalty = mem / 10 + max(0, (mem - 85) / 15)

            cpu_score = max(0.0, min(10.0, 10 - cpu_penalty))
            mem_score = max(0.0, min(10.0, 10 - mem_penalty))

            return round(cpu_score * 0.6 + mem_score * 0.4, 2)
        except Exception:
            return 5.0

    def get_wifi_signal(self, ssid: Optional[str] = None) -> float:
        """
        Força do sinal Wi-Fi [0, 10].
        Retorna 5.0 se não conseguir medir (valor neutro).
        Requer instalação opcional: pip install nano-wait[wifi]
        """
        try:
            if self.system == "windows":
                self._init_wifi()
                if self._wifi_interface:
                    self._wifi_interface.scan()
                    time.sleep(0.4)
                    for net in self._wifi_interface.scan_results():
                        if ssid is None or net.ssid == ssid:
                            return max(0.0, min(10.0, (net.signal + 100) / 10))

            elif self.system == "darwin":
                cmd = [
                    "/System/Library/PrivateFrameworks/Apple80211.framework"
                    "/Versions/Current/Resources/airport", "-I"
                ]
                out = subprocess.check_output(cmd, text=True, timeout=2)
                for line in out.splitlines():
                    if "agrCtlRSSI" in line:
                        rssi = int(line.split(":")[1].strip())
                        return max(0.0, min(10.0, (rssi + 100) / 10))

            elif self.system == "linux":
                out = subprocess.check_output(
                    ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"],
                    text=True, timeout=2
                )
                for line in out.splitlines():
                    parts = line.split(":")
                    if len(parts) >= 3:
                        active, name, sig = parts[0], parts[1], parts[2]
                        if active == "yes" or (ssid and name == ssid):
                            return max(0.0, min(10.0, int(sig) / 10))
        except Exception:
            pass
        return 5.0

    # ──────────────────────────────────────────
    # Snapshot de Contexto (com cache TTL)
    # ──────────────────────────────────────────

    def snapshot_context(self, ssid: Optional[str] = None) -> Dict[str, Any]:
        """
        Captura estado imutável do ambiente para análise determinística.
        Usa cache com TTL de 2s para evitar coletas redundantes em loops de polling.
        """
        now = time.time()
        if self._ctx_cache is not None and (now - self._ctx_ts) < self.CONTEXT_TTL:
            return self._ctx_cache

        ctx = {
            "pc_score":   self.get_pc_score(),
            "wifi_score": self.get_wifi_signal(ssid) if ssid else None,
            "timestamp":  now,
        }
        self._ctx_cache = ctx
        self._ctx_ts = now
        return ctx

    def invalidate_context(self):
        """Força nova coleta de contexto na próxima chamada."""
        self._ctx_cache = None

    # ──────────────────────────────────────────
    # Cálculo de Velocidade
    # ──────────────────────────────────────────

    def smart_speed(self, ssid: Optional[str] = None) -> float:
        """
        Fator de velocidade adaptativo [0.5, 6.0] baseado em saúde do sistema.
        Sistema saudável → fator maior → espera menor.
        """
        ctx = self.snapshot_context(ssid)
        pc   = ctx["pc_score"]
        wifi = ctx["wifi_score"] if ctx["wifi_score"] is not None else 5.0
        health = (pc + wifi) / 2
        return round(max(0.5, min(6.0, health / 2 + 0.5)), 2)

    # ──────────────────────────────────────────
    # Cálculo de Espera — CORRIGIDO
    # ──────────────────────────────────────────

    def compute_wait(
        self,
        base_time: float,
        speed_factor: float,
        context: Dict[str, Any],
        smart: bool = False,
    ) -> float:
        """
        Lógica central: calcula o tempo final de espera.

        Modo smart=False (padrão):
            Nunca reduz abaixo do tempo pedido.
            Só aumenta quando o sistema está sobrecarregado (health < 5).
            Garante previsibilidade para testes e automação.

            WaitTime = base_time * (1 + overload_penalty) * aggressiveness

        Modo smart=True:
            Pode reduzir o tempo em sistemas ociosos.
            Útil quando a espera é uma cortesia, não um requisito.

            WaitTime = base_time * adaptive_multiplier * aggressiveness
        """
        pc   = context["pc_score"]
        wifi = context["wifi_score"] if context["wifi_score"] is not None else 5.0
        health = (pc + wifi) / 2

        if smart:
            # Pode reduzir: sistema saudável → espera menor
            adaptive_multiplier = max(0.05, (10 - health) / max(0.1, speed_factor))
            return self.apply_profile(base_time * adaptive_multiplier)
        else:
            # Nunca reduz: só penaliza sistema sobrecarregado (health < 5)
            overload_penalty = max(0.0, (5.0 - health) / 5.0)
            multiplier = 1.0 + overload_penalty
            return self.apply_profile(base_time * multiplier)

    def compute_wait_no_wifi(
        self,
        speed_factor: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Variante sem Wi-Fi: usa apenas pc_score como saúde.
        Retorna um multiplicador (fator), não um tempo absoluto.
        """
        if context is None:
            context = self.snapshot_context()
        pc = context["pc_score"]
        health = pc
        return max(0.1, health / max(0.1, speed_factor))

    def compute_wait_wifi(
        self,
        speed_factor: float,
        ssid: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Variante com Wi-Fi: usa pc_score + wifi_score como saúde.
        Retorna um multiplicador (fator), não um tempo absoluto.
        """
        if context is None:
            context = self.snapshot_context(ssid)
        pc   = context["pc_score"]
        wifi = context["wifi_score"] if context["wifi_score"] is not None else 5.0
        health = (pc + wifi) / 2
        return max(0.1, health / max(0.1, speed_factor))

    def apply_profile(self, wait_time: float) -> float:
        """Ajusta o tempo conforme o perfil de execução ativo."""
        return wait_time * self.profile.aggressiveness