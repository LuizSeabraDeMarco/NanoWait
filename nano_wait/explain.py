"""
NanoWait Explain Mode
--------------------
Gera relatórios detalhados sobre as decisões tomadas pelo motor.
Útil para depuração de performance e auditoria de automação.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
import json

@dataclass
class ExplainReport:
    """Relatório detalhado de uma operação de espera ou execução."""
    requested_time: Optional[float]
    final_time: float
    speed_input: Any
    speed_value: float
    smart: bool
    cpu_score: float
    wifi_score: Optional[float]
    factor: float
    min_floor_applied: bool
    max_cap_applied: bool
    timestamp: str
    nano_wait_version: str = "6.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """Converte o relatório para um dicionário serializável."""
        return asdict(self)

    def to_json(self) -> str:
        """Converte o relatório para uma string JSON formatada."""
        return json.dumps(self.to_dict(), indent=2)

    def explain(self) -> str:
        """Gera uma explicação humanizada das decisões do motor."""
        report = [
            f"🚀 NanoWait Explain Mode (v{self.nano_wait_version})",
            f"📅 Timestamp: {self.timestamp}",
            "-" * 40,
            f"⏱ Tempo solicitado: {self.requested_time if self.requested_time is not None else 'N/A'}s",
            f"✅ Tempo final executado: {self.final_time:.4f}s",
            f"⚡ Velocidade configurada: {self.speed_input} (valor: {self.speed_value})",
            f"🧠 Modo Inteligente (Smart): {'Ativado' if self.smart else 'Desativado'}",
            "-" * 40,
            "🔍 Contexto do Sistema:",
            f"  💻 CPU Score: {self.cpu_score}/10",
            f"  🌐 Wi-Fi Score: {self.wifi_score if self.wifi_score is not None else 'N/A'}/10",
            f"  📊 Fator Adaptativo Calculado: {self.factor:.4f}",
            "-" * 40,
            "💡 Decisões Internas:",
            f"  - Piso mínimo aplicado: {'Sim' if self.min_floor_applied else 'Não'}",
            f"  - Teto máximo aplicado: {'Sim' if self.max_cap_applied else 'Não'}",
            f"  - Resultado: {'Otimizado' if self.final_time < (self.requested_time or 0) else 'Conservador'}",
            "-" * 40
        ]
        return "\n".join(report)

    def __str__(self) -> str:
        return self.explain()
