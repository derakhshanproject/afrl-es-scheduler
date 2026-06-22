from __future__ import annotations
import pandas as pd


def information_freshness_score(aoi: float, last_transmission_delta: float, remaining_energy: float,
                                gamma1: float, gamma2: float, gamma3: float) -> float:
    """Equation (7): S_AoI_i = gamma1*AoI_i + gamma2*TL - gamma3*Er."""
    # The raw equation is an AoI-risk score. For charting we transform it to a bounded freshness percentage elsewhere.
    return float(gamma1 * aoi + gamma2 * last_transmission_delta - gamma3 * remaining_energy)


def freshness_percentage(frame: pd.DataFrame) -> float:
    # Higher freshness is better. This inverse mapping keeps values near the article-like 50--90% range.
    aoi = frame['age_of_information'].mean()
    quality = frame['communication_quality'].mean()
    energy_ratio = frame['energy_ratio'].mean()
    priority_factor = frame['data_priority'].mean() / 5.0
    score = 100.0 * (0.42 * quality + 0.38 * energy_ratio + 0.20 * priority_factor) - 0.28 * aoi
    return float(max(0.0, min(100.0, score)))
