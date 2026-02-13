from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class ExplainReport:
    requested_time: Optional[float]
    final_time: float

    speed_input: str | float
    speed_value: float
    smart: bool

    cpu_score: float
    wifi_score: Optional[float]
    factor: float

    min_floor_applied: bool
    max_cap_applied: bool

    timestamp: str
    nano_wait_version: str = "5.0.2"

    def to_dict(self):
        return asdict(self)

    def explain(self) -> str:
        lines = [
            f"Requested time: {self.requested_time}s",
            f"Final wait time: {self.final_time}s",
            f"Speed input: {self.speed_input} → {self.speed_value}",
            f"Smart mode: {self.smart}",
            f"CPU score: {self.cpu_score}",
        ]

        if self.wifi_score is not None:
            lines.append(f"Wi-Fi score: {self.wifi_score}")

        lines.extend([
            f"Adaptive factor: {self.factor}",
            f"Minimum floor applied: {self.min_floor_applied}",
            f"Maximum cap applied: {self.max_cap_applied}",
            f"Timestamp: {self.timestamp}",
        ])

        return "\n".join(lines)
