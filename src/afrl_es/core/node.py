from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np


@dataclass(slots=True)
class IoTNode:
    """State of an IoT node in the AFRL-ES simulation."""
    node_id: int
    initial_energy: float
    remaining_energy: float
    data_priority: int
    communication_quality: float
    bandwidth_mbps: float
    processing_cost: float
    processing_delay_ms: float
    packet_size_kb: float
    power_consumption: float
    transmission_rate_mbps: float
    last_transmission_time: int = 0
    waiting_time_ms: float = 0.0
    period: int = 5
    packet_counter: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def age_of_information(self, current_time: int) -> float:
        return max(0.0, float(current_time - self.last_transmission_time))

    def time_since_last_transmission(self, current_time: int) -> float:
        return self.age_of_information(current_time)

    def is_energy_eligible(self, threshold_ratio: float) -> bool:
        return self.remaining_energy >= threshold_ratio * self.initial_energy

    def update_dynamic_conditions(self, rng: np.random.Generator, quality_noise_std: float, bandwidth_noise_std_ratio: float) -> None:
        self.communication_quality = float(np.clip(self.communication_quality + rng.normal(0.0, quality_noise_std), 0.01, 1.0))
        self.bandwidth_mbps = float(max(0.1, self.bandwidth_mbps * (1.0 + rng.normal(0.0, bandwidth_noise_std_ratio))))
        self.processing_delay_ms = float(max(0.1, self.processing_delay_ms * (1.0 + rng.normal(0.0, 0.03))))

    def consume_idle_energy(self, idle_cost: float) -> None:
        self.remaining_energy = float(max(0.0, self.remaining_energy - idle_cost))

    def consume_transmission_energy(self, base_cost: float, processing_scale: float) -> None:
        cost = base_cost + processing_scale * self.processing_cost + 0.0001 * self.packet_size_kb
        self.remaining_energy = float(max(0.0, self.remaining_energy - cost))

    def maybe_recover_energy(self, rng: np.random.Generator, probability: float, amount_range: tuple[float, float]) -> None:
        if rng.random() < probability:
            self.remaining_energy = float(min(self.initial_energy, self.remaining_energy + rng.uniform(*amount_range)))

    def should_generate_packet(self, current_time: int, rng: np.random.Generator, burst_probability: float) -> bool:
        periodic = current_time % max(1, self.period) == 0
        burst = rng.random() < burst_probability
        return periodic or burst

    def as_observation(self, current_time: int) -> dict[str, float | int]:
        return {
            'node_id': self.node_id,
            'time_step': current_time,
            'age_of_information': self.age_of_information(current_time),
            'remaining_energy': self.remaining_energy,
            'energy_ratio': self.remaining_energy / max(self.initial_energy, 1e-12),
            'data_priority': self.data_priority,
            'communication_quality': self.communication_quality,
            'bandwidth_mbps': self.bandwidth_mbps,
            'processing_cost': self.processing_cost,
            'processing_delay_ms': self.processing_delay_ms,
            'packet_size_kb': self.packet_size_kb,
            'power_consumption': self.power_consumption,
            'transmission_rate_mbps': self.transmission_rate_mbps,
            'last_transmission_time': self.last_transmission_time,
            'waiting_time_ms': self.waiting_time_ms,
        }
