# telemetry.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass(frozen=True)
class TelemetryEvent:
    timestamp: str
    factor: float
    interval: float


@dataclass
class TelemetrySession:
    """
    Local, optional and ephemeral telemetry session.
    No remote collection. No persistence by default.
    """

    enabled: bool = False
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    cpu_score: Optional[float] = None
    wifi_score: Optional[float] = None
    profile: Optional[str] = None

    events: List[TelemetryEvent] = field(default_factory=list)

    def start(self):
        if self.enabled:
            from time import time
            self.start_time = time()

    def stop(self):
        if self.enabled:
            from time import time
            self.end_time = time()

    def record(self, *, factor: float, interval: float):
        if not self.enabled:
            return

        self.events.append(
            TelemetryEvent(
                timestamp=datetime.utcnow().isoformat(),
                factor=round(factor, 4),
                interval=round(interval, 4),
            )
        )

    def summary(self) -> dict:
        if not self.enabled:
            return {}

        total_time = (
            round(self.end_time - self.start_time, 4)
            if self.start_time and self.end_time
            else None
        )

        return {
            "profile": self.profile,
            "cpu_score": self.cpu_score,
            "wifi_score": self.wifi_score,
            "adjustments": len(self.events),
            "total_time": total_time,
        }
