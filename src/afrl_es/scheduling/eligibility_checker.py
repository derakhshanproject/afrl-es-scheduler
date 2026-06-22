from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class EligibilityChecker:
    energy_threshold_ratio: float
    quality_threshold: float
    qos_threshold: float = 0.80

    def mark_eligible(self, frame: pd.DataFrame) -> pd.DataFrame:
        out = frame.copy()
        energy_ok = out['energy_ratio'] >= self.energy_threshold_ratio
        quality_ok = out['communication_quality'] >= self.quality_threshold
        out['eligible'] = energy_ok & quality_ok
        out['defer_reason'] = ''
        out.loc[~energy_ok, 'defer_reason'] = 'low_energy'
        out.loc[energy_ok & ~quality_ok, 'defer_reason'] = 'low_link_quality'
        return out
