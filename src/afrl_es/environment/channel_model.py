from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from afrl_es.core.node import IoTNode


@dataclass(slots=True)
class ChannelModel:
    quality_noise_std: float
    bandwidth_noise_std_ratio: float
    congestion_base: float
    congestion_node_scale: float

    def update(self, nodes: list[IoTNode], rng: np.random.Generator) -> float:
        congestion = min(0.90, self.congestion_base + self.congestion_node_scale * len(nodes))
        for node in nodes:
            node.update_dynamic_conditions(rng, self.quality_noise_std, self.bandwidth_noise_std_ratio)
            node.communication_quality = float(np.clip(node.communication_quality * (1.0 - 0.25 * congestion), 0.01, 1.0))
            node.waiting_time_ms = float(max(0.0, node.waiting_time_ms + rng.normal(congestion * 5.0, 1.0)))
        return congestion
