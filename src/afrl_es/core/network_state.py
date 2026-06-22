from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .node import IoTNode


@dataclass(slots=True)
class NetworkState:
    """Snapshot of the active IoT network."""
    time_step: int
    nodes: list[IoTNode]

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([node.as_observation(self.time_step) for node in self.nodes])

    @property
    def number_of_nodes(self) -> int:
        return len(self.nodes)
