from __future__ import annotations
import pandas as pd


def estimate_processing_transmission_time(waiting_time_ms: float, processing_cost: float, processing_delay_ms: float,
                                          transmission_rate_mbps: float, importance_weight: float,
                                          packet_size_kb: float, bandwidth_mbps: float) -> float:
    """Equation (4): T_i = W_{i-1} * ((C_i + D_i)/R_i) + eps_i*(L_i/B_i).

    Units are simulation-normalized. The project stores this as milliseconds-equivalent.
    """
    transmission_rate_mbps = max(transmission_rate_mbps, 1e-9)
    bandwidth_mbps = max(bandwidth_mbps, 1e-9)
    return float(waiting_time_ms * ((processing_cost + processing_delay_ms) / transmission_rate_mbps) + importance_weight * (packet_size_kb / bandwidth_mbps))


def add_processing_time(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out['processing_transmission_time'] = [
        estimate_processing_transmission_time(
            row.waiting_time_ms,
            row.processing_cost,
            row.processing_delay_ms,
            row.transmission_rate_mbps,
            max(1.0, row.data_priority / 5.0),
            row.packet_size_kb,
            row.bandwidth_mbps,
        )
        for row in out.itertuples(index=False)
    ]
    return out
