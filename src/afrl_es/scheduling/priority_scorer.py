from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(slots=True)
class PriorityWeights:
    w1_aoi: float
    w2_priority: float
    w3_energy: float
    w4_quality: float

    def as_array(self) -> np.ndarray:
        return np.array([self.w1_aoi, self.w2_priority, self.w3_energy, self.w4_quality], dtype=float)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'PriorityWeights':
        arr = np.asarray(arr, dtype=float)
        return cls(float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]))


@dataclass(slots=True)
class OverallPriorityWeights:
    theta1_last_transmission: float
    theta2_aoi: float
    theta3_priority: float
    theta4_energy: float


def node_priority_score(aoi: float, priority: float, remaining_energy: float, communication_quality: float, weights: PriorityWeights) -> float:
    """Equation (1): S_i = w1*AoI_i + w2*Pr_i - w3*Er_i - w4*Qc_i."""
    return (
        weights.w1_aoi * aoi
        + weights.w2_priority * priority
        - weights.w3_energy * remaining_energy
        - weights.w4_quality * communication_quality
    )


def overall_priority_score(last_transmission_time: float, aoi: float, priority: float, remaining_energy: float, weights: OverallPriorityWeights) -> float:
    """Equation (2): Sc_i = theta1*TL + theta2*AoI_i + theta3*Pr_i - theta4*Er_i."""
    return (
        weights.theta1_last_transmission * last_transmission_time
        + weights.theta2_aoi * aoi
        + weights.theta3_priority * priority
        - weights.theta4_energy * remaining_energy
    )


def optimal_transmission_objective(aoi_values: np.ndarray, priority_values: np.ndarray, energy_values: np.ndarray) -> float:
    """Equation (3): minimize sum(AoI_i + Pr_i - Er_i)."""
    return float(np.sum(np.asarray(aoi_values) + np.asarray(priority_values) - np.asarray(energy_values)))


def score_frame(frame: pd.DataFrame, weights: PriorityWeights, overall_weights: OverallPriorityWeights) -> pd.DataFrame:
    out = frame.copy()
    out['priority_score'] = (
        weights.w1_aoi * out['age_of_information']
        + weights.w2_priority * out['data_priority']
        - weights.w3_energy * out['remaining_energy']
        - weights.w4_quality * out['communication_quality']
    )
    out['overall_priority_score'] = (
        overall_weights.theta1_last_transmission * out['last_transmission_time']
        + overall_weights.theta2_aoi * out['age_of_information']
        + overall_weights.theta3_priority * out['data_priority']
        - overall_weights.theta4_energy * out['remaining_energy']
    )
    # Combined score keeps article Equation 1 central while using Equation 2 as an auxiliary signal.
    out['combined_priority_score'] = 0.65 * out['priority_score'] + 0.35 * out['overall_priority_score']
    return out
