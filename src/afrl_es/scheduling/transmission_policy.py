from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class TransmissionPolicy:
    scheduler_capacity_ratio: float
    minimum_scheduler_capacity: int
    method_capacity_factor: float = 1.0

    def capacity(self, n_nodes: int) -> int:
        return max(self.minimum_scheduler_capacity, int(round(n_nodes * self.scheduler_capacity_ratio * self.method_capacity_factor)))

    def select(self, scored_frame: pd.DataFrame) -> pd.DataFrame:
        cap = self.capacity(len(scored_frame))
        eligible = scored_frame[scored_frame['eligible']].copy()
        selected_ids = set(eligible.sort_values('combined_priority_score', ascending=False).head(cap)['node_id'].tolist())
        out = scored_frame.copy()
        out['scheduled'] = out['node_id'].isin(selected_ids)
        return out
