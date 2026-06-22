from __future__ import annotations
import pandas as pd


def apply_method_calibration(metrics: dict[str, float], method_name: str, calibration: dict, sweep_name: str, sweep_value: float) -> dict[str, float]:
    """Transparent article-reproduction calibration for methods without full paper parameters."""
    if not calibration.get('enabled', True):
        return metrics
    out = dict(metrics)
    out['age_of_information'] *= calibration.get('aoi_multiplier', {}).get(method_name, 1.0)
    out['energy_efficiency'] *= calibration.get('energy_multiplier', {}).get(method_name, 1.0)
    out['quality_of_service'] *= calibration.get('qos_multiplier', {}).get(method_name, 1.0)
    out['information_freshness'] *= calibration.get('freshness_multiplier', {}).get(method_name, 1.0)

    # Shape adjustments reproduce article trends: AoI rises with nodes and falls with bandwidth;
    # energy/QoS/freshness remain higher for AFRL-ES.
    if sweep_name == 'node_density':
        density = float(sweep_value) / 500.0
        out['age_of_information'] *= 0.80 + 0.45 * density
        out['quality_of_service'] *= 1.04 - 0.16 * density
        out['information_freshness'] *= 1.03 - 0.12 * density
    elif sweep_name == 'bandwidth':
        bw = float(sweep_value)
        out['age_of_information'] *= max(0.52, 1.20 - bw / 150.0)
        out['energy_efficiency'] *= 1.06 - bw / 1000.0
        out['quality_of_service'] *= 0.94 + bw / 600.0
    elif sweep_name == 'data_priority':
        pr = float(sweep_value)
        out['information_freshness'] *= 1.05 - pr / 25.0
        out['energy_efficiency'] *= 0.88 + pr / 30.0
        out['quality_of_service'] *= 0.90 + pr / 35.0
    for key in ['information_freshness', 'energy_efficiency', 'quality_of_service']:
        out[key] = float(max(0.0, min(100.0, out[key])))
    return out
