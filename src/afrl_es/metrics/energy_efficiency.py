from __future__ import annotations
import pandas as pd


def energy_efficiency(remaining_energy: float, power_consumption: float, processing_cost: float) -> float:
    """Equation (8): Ef_i = Er_i / (P_i + C_i)."""
    return float(remaining_energy / max(power_consumption + processing_cost, 1e-12))


def energy_score(remaining_energy: float, processing_cost: float, power_consumption: float,
                 delta1: float, delta2: float) -> float:
    """Equation (9): S_En_i = delta1*(Er_i/C_i) - delta2*P_i."""
    return float(delta1 * (remaining_energy / max(processing_cost, 1e-12)) - delta2 * power_consumption)


def energy_efficiency_percentage(frame: pd.DataFrame) -> float:
    initial = frame['remaining_energy'] / frame['energy_ratio'].clip(lower=1e-9)
    ratio = (frame['remaining_energy'] / initial.clip(lower=1e-9)).mean()
    penalty = 0.08 * frame['power_consumption'].mean() + 0.05 * frame['processing_cost'].mean()
    return float(max(0.0, min(100.0, 100.0 * ratio - 100.0 * penalty)))
