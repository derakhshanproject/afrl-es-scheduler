from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class ExponentialPredictionModel:
    """Small value predictor used by the lightweight RL update rule."""
    momentum: float = 0.90
    value: float = 0.0
    initialized: bool = False

    def predict(self) -> float:
        return float(self.value)

    def update(self, observed_reward: float) -> float:
        if not self.initialized:
            self.value = float(observed_reward)
            self.initialized = True
        else:
            self.value = float(self.momentum * self.value + (1.0 - self.momentum) * observed_reward)
        return self.value
