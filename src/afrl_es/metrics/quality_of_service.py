from __future__ import annotations
import pandas as pd


def qos_score(delay_ms: float, bandwidth_mbps: float, remaining_energy: float,
              rho1: float, rho2: float, rho3: float, mode: str = 'article_exact') -> float:
    """Equation (10), with article-exact and corrected alternatives.

    article_exact: S_QoS_i = rho1*(1/D_i) - rho2*B_i - rho3*Er_i
    corrected:     S_QoS_i = rho1*(1/D_i) + rho2*B_i + rho3*Er_i
    """
    delay_term = rho1 * (1.0 / max(delay_ms, 1e-12))
    if mode == 'article_exact':
        return float(delay_term - rho2 * bandwidth_mbps - rho3 * remaining_energy)
    if mode == 'corrected':
        return float(delay_term + rho2 * bandwidth_mbps + rho3 * remaining_energy)
    raise ValueError(f"Unknown QoS formula mode: {mode}")


def qos_percentage(frame: pd.DataFrame) -> float:
    delay = frame['processing_delay_ms'].mean()
    quality = frame['communication_quality'].mean()
    energy_ratio = frame['energy_ratio'].mean()
    bandwidth = frame['bandwidth_mbps'].mean()
    # Higher is better. Normalize against a broad IoT edge simulation range.
    delay_component = max(0.0, 1.0 - delay / 80.0)
    bandwidth_component = min(1.0, bandwidth / 100.0)
    score = 100.0 * (0.35 * quality + 0.25 * energy_ratio + 0.25 * delay_component + 0.15 * bandwidth_component)
    return float(max(0.0, min(100.0, score)))
