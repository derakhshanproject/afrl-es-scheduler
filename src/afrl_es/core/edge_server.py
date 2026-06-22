from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from .node import IoTNode


@dataclass(slots=True)
class EdgeServer:
    """Edge-side processing unit for scheduled IoT transmissions."""
    high_priority_cutoff: int = 4
    cache_high_priority_data: bool = True
    filtering_ratio_low_priority: float = 0.18
    local_processing_delay_reduction: float = 0.18
    edge_energy_saving_ratio: float = 0.10
    cache: dict[int, dict] = field(default_factory=dict)
    processed_packets: int = 0
    filtered_packets: int = 0

    def process_scheduled_nodes(self, nodes: Iterable[IoTNode], current_time: int) -> list[dict]:
        records: list[dict] = []
        for node in nodes:
            original_delay = node.processing_delay_ms
            if node.data_priority >= self.high_priority_cutoff and self.cache_high_priority_data:
                self.cache[node.node_id] = {'time_step': current_time, 'priority': node.data_priority}
            elif node.data_priority < self.high_priority_cutoff:
                self.filtered_packets += 1 if self.filtering_ratio_low_priority > 0 else 0
            node.processing_delay_ms = max(0.1, node.processing_delay_ms * (1.0 - self.local_processing_delay_reduction))
            self.processed_packets += 1
            records.append({
                'node_id': node.node_id,
                'time_step': current_time,
                'original_processing_delay_ms': original_delay,
                'edge_processing_delay_ms': node.processing_delay_ms,
                'cached': node.node_id in self.cache,
            })
        return records
