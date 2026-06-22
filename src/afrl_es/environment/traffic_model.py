from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from afrl_es.core.node import IoTNode


@dataclass(slots=True)
class TrafficModel:
    burst_probability: float
    high_priority_cutoff: int
    burst_priority_boost_probability: float

    def update_priorities(self, nodes: list[IoTNode], current_time: int, rng: np.random.Generator, fixed_priority: int | None = None) -> None:
        for node in nodes:
            if fixed_priority is not None:
                node.data_priority = int(fixed_priority)
                continue
            if node.should_generate_packet(current_time, rng, self.burst_probability):
                if rng.random() < self.burst_priority_boost_probability:
                    node.data_priority = int(rng.integers(self.high_priority_cutoff, 6))
                else:
                    node.data_priority = int(rng.integers(1, 6))
                node.packet_counter += 1
