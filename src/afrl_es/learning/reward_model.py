from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class RewardWeights:
    lambda1_qos: float
    lambda2_aoi: float
    lambda3_energy_efficiency: float


def reward(qos: float, aoi: float, energy_efficiency: float, weights: RewardWeights) -> float:
    """Article reward: R_i = lambda1*QoS - lambda2*AoI + lambda3*Ef_i."""
    return float(weights.lambda1_qos * qos - weights.lambda2_aoi * aoi + weights.lambda3_energy_efficiency * energy_efficiency)
