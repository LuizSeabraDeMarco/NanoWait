"""
NanoWait Core Engine
--------------------
Base teórica: O NanoWait opera sob o princípio de "Observabilidade de Execução". 
Diferente de um sleep estático, ele utiliza telemetria em tempo real (CPU, Memória, Rede) 
para calcular o "Custo de Oportunidade de Espera". 

A fórmula base segue uma relação inversamente proporcional à saúde do sistema:
WaitTime = (BaseTime / (SystemHealth * NetworkStability)) * ProfileAggressiveness
"""

import platform
import time
import subprocess
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class ExecutionProfile:
    """Define o comportamento de agressividade e tolerância do motor."""
    name: str
    aggressiveness: float      # Multiplicador para intervalos adaptativos (menor = mais rápido)
    tolerance: float           # Permissividade a falhas temporárias (0.0 a 1.0)
    poll_interval: float       # Base para loops de polling em segundos
    verbose: bool              # Ativa logs detalhados por padrão

PROFILES: Dict[str, ExecutionProfile] = {
    "ci": ExecutionProfile("ci", 0.5, 0.9, 0.05, True),
    "testing": ExecutionProfile("testing", 1.0, 0.7, 0.1, True),
    "rpa": ExecutionProfile("rpa", 2.0, 0.5, 0.2, False),
    "default": ExecutionProfile("default", 1.0, 0.8, 0.1, False),
}

class NanoWait:
    """
    O motor central que orquestra a coleta de contexto e ajuste de timing.
    """
    def __init__(self, profile: Optional[str] = None):
        self.system = platform.system().lower()
        self.profile = PROFILES.get(profile, PROFILES["default"])
        self._wifi_interface = None
        self._initialized_wifi = False

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

    def get_pc_score(self) -> float:
        """
        Calcula o score de performance do sistema (0-10).
        10 = Sistema ocioso e rápido. 0 = Sistema sob estresse extremo.
        """
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.1) # Reduzido interval para maior responsividade
            mem = psutil.virtual_memory().percent
            
            # Penalidade não linear para estresse alto
            cpu_score = max(0, min(10, 10 - (cpu / 10)))
            mem_score = max(0, min(10, 10 - (mem / 10)))
            
            return round((cpu_score * 0.6) + (mem_score * 0.4), 2)
        except Exception:
            return 5.0

    def get_wifi_signal(self, ssid: Optional[str] = None) -> float:
        """
        Retorna a força do sinal Wi-Fi (0-10).
        """
        try:
            if self.system == "windows":
                self._init_wifi()
                if self._wifi_interface:
                    self._wifi_interface.scan()
                    time.sleep(0.5) # Reduzido de 2s para 0.5s
                    for net in self._wifi_interface.scan_results():
                        if ssid is None or net.ssid == ssid:
                            return max(0, min(10, (net.signal + 100) / 10))

            elif self.system == "darwin":
                cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
                out = subprocess.check_output(cmd, text=True)
                for line in out.splitlines():
                    if "agrCtlRSSI" in line:
                        rssi = int(line.split(":")[1].strip())
                        return max(0, min(10, (rssi + 100) / 10))

            elif self.system == "linux":
                out = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"], text=True)
                for line in out.splitlines():
                    parts = line.split(":")
                    if len(parts) >= 3:
                        active, name, sig = parts[0], parts[1], parts[2]
                        if active == "yes" or (ssid and name == ssid):
                            return max(0, min(10, int(sig) / 10))
        except Exception:
            pass
        return 5.0

    def snapshot_context(self, ssid: Optional[str] = None) -> Dict[str, Any]:
        """Captura um estado imutável do ambiente para análise determinística."""
        return {
            "pc_score": self.get_pc_score(),
            "wifi_score": self.get_wifi_signal(ssid) if ssid else None,
            "timestamp": time.time()
        }

    def smart_speed(self, ssid: Optional[str] = None) -> float:
        """Calcula o fator de velocidade adaptativo (0.5 - 5.0)."""
        ctx = self.snapshot_context(ssid)
        pc = ctx["pc_score"]
        wifi = ctx["wifi_score"] if ctx["wifi_score"] is not None else 5.0
        
        # Heurística: se o sistema está lento, diminuímos a velocidade (aumentamos a espera)
        # Se o sistema está rápido, aumentamos a velocidade (diminuímos a espera)
        health = (pc + wifi) / 2
        return round(max(0.5, min(5.0, health / 2)), 2)

    def compute_wait(self, base_time: float, speed_factor: float, context: Dict[str, Any]) -> float:
        """Aplica a lógica teórica central para calcular o tempo final de espera."""
        pc = context["pc_score"]
        wifi = context["wifi_score"] if context["wifi_score"] is not None else 5.0
        
        # Quanto maior a saúde (pc+wifi), menor o multiplicador de espera
        health_factor = (pc + wifi) / 2
        # Evita divisão por zero e garante um piso de segurança
        adaptive_multiplier = max(0.1, (10 - health_factor) / max(0.1, speed_factor))
        
        final_wait = base_time * adaptive_multiplier
        return self.apply_profile(final_wait)

    def apply_profile(self, wait_time: float) -> float:
        """Ajusta o tempo conforme o perfil de execução ativo."""
        return wait_time * self.profile.aggressiveness
