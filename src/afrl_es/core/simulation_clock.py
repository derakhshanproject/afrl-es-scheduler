from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class SimulationClock:
    current_time: int = 0
    time_step_seconds: float = 1.0

    def tick(self) -> int:
        self.current_time += 1
        return self.current_time
