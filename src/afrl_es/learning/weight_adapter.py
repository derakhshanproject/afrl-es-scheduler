from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from afrl_es.scheduling.priority_scorer import PriorityWeights


@dataclass(slots=True)
class WeightAdapter:
    """Lightweight reinforcement-learning coefficient updater.

    Implements Equation (5): w_new = w_old + alpha*(R - P).
    The update is projected to a stable range and optionally normalized.
    """
    alpha: float
    weight_min: float
    weight_max: float
    normalize_weights: bool = True

    def update(self, weights: PriorityWeights, reward_value: float, predicted_value: float) -> PriorityWeights:
        arr = weights.as_array()
        error = float(reward_value - predicted_value)
        # Directional adaptation: AoI and priority increase with positive reward error;
        # energy/quality penalties become sharper when reward error is negative.
        direction = np.array([1.0, 0.85, -0.45, -0.35], dtype=float)
        new_arr = arr + self.alpha * error * 0.001 * direction
        new_arr = np.clip(new_arr, self.weight_min, self.weight_max)
        if self.normalize_weights:
            s = new_arr.sum()
            if s > 0:
                new_arr = new_arr / s
        return PriorityWeights.from_array(new_arr)
