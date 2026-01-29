from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import queue as std_queue

from .usage import log_usage_event

@dataclass(frozen=True)
class TelemetryEvent:
    timestamp: str
    factor: float
    interval: float


@dataclass
class TelemetrySession:
    enabled: bool = False
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    cpu_score: Optional[float] = None
    wifi_score: Optional[float] = None
    profile: Optional[str] = None

    events: List[TelemetryEvent] = field(default_factory=list)

    queue: Optional[std_queue.Queue] = None

    def start(self):
        if not self.enabled:
            return

        from time import time
        self.start_time = time()

        # 🔹 ONE usage event per execution (MAU signal)
        log_usage_event("session_start", __version__)

    def stop(self):
        if not self.enabled:
            return

        from time import time
        self.end_time = time()

        if self.queue:
            self.queue.put("__STOP__")

    def record(self, *, factor: float, interval: float):
        if not self.enabled:
            return

        event = TelemetryEvent(
            timestamp=datetime.utcnow().isoformat(),
            factor=round(factor, 4),
            interval=round(interval, 4),
        )

        self.events.append(event)

        if self.queue:
            self.queue.put({
                "factor": event.factor,
                "interval": event.interval,
                "count": len(self.events)
            })

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
