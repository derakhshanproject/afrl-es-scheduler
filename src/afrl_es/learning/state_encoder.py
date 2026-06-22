from __future__ import annotations
import numpy as np
import pandas as pd


def encode_state(frame: pd.DataFrame) -> np.ndarray:
    """Article state: s_t = {AoI_i, Er_i, Pr_i, Qc_i}, aggregated to network-level features."""
    return np.array([
        frame['age_of_information'].mean(),
        frame['remaining_energy'].mean(),
        frame['data_priority'].mean(),
        frame['communication_quality'].mean(),
    ], dtype=float)


def normalize_state(state: np.ndarray) -> np.ndarray:
    scale = np.array([100.0, 120.0, 5.0, 1.0], dtype=float)
    return np.asarray(state, dtype=float) / scale
