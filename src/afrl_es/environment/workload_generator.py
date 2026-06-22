from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from afrl_es.core.node import IoTNode


@dataclass(slots=True)
class WorkloadGenerator:
    cfg: dict
    rng: np.random.Generator

    def create_nodes(self, number_of_nodes: int, bandwidth_mbps: float, fixed_priority: int | None = None) -> list[IoTNode]:
        init = self.cfg['node_initialization']
        traffic = self.cfg['traffic']
        nodes: list[IoTNode] = []
        for node_id in range(number_of_nodes):
            initial_energy = float(self.rng.uniform(*init['initial_energy_range']))
            priority = int(fixed_priority) if fixed_priority is not None else int(self.rng.choice(init['data_priority_levels']))
            node = IoTNode(
                node_id=node_id,
                initial_energy=initial_energy,
                remaining_energy=initial_energy,
                data_priority=priority,
                communication_quality=float(self.rng.uniform(*init['communication_quality_range'])),
                bandwidth_mbps=float(max(0.1, self.rng.normal(bandwidth_mbps, bandwidth_mbps * 0.05))),
                processing_cost=float(self.rng.uniform(*init['processing_cost_range'])),
                processing_delay_ms=float(self.rng.uniform(*init['processing_delay_range_ms'])),
                packet_size_kb=float(self.rng.uniform(*init['packet_size_range_kb'])),
                power_consumption=float(self.rng.uniform(*init['power_consumption_range'])),
                transmission_rate_mbps=float(self.rng.uniform(*init['transmission_rate_range_mbps'])),
                last_transmission_time=0,
                waiting_time_ms=float(self.rng.uniform(*init['waiting_time_range_ms'])),
                period=int(self.rng.integers(traffic['period_range'][0], traffic['period_range'][1] + 1)),
            )
            nodes.append(node)
        return nodes
