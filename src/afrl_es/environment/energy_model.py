from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from afrl_es.core.node import IoTNode


@dataclass(slots=True)
class EnergyModel:
    idle_cost_per_episode: float
    active_transmission_cost: float
    processing_energy_scale: float
    recovery_probability: float
    recovery_amount_range: tuple[float, float]

    def idle_update(self, nodes: list[IoTNode], rng: np.random.Generator) -> None:
        for node in nodes:
            node.consume_idle_energy(self.idle_cost_per_episode)
            node.maybe_recover_energy(rng, self.recovery_probability, self.recovery_amount_range)

    def transmission_update(self, nodes: list[IoTNode]) -> None:
        for node in nodes:
            node.consume_transmission_energy(self.active_transmission_cost, self.processing_energy_scale)
