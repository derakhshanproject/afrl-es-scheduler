from __future__ import annotations
import pandas as pd


def age_of_information(current_time: int, last_transmission_time: int) -> float:
    """Equation (6): AoI_i(t) = t - t_i,last."""
    return float(max(0, current_time - last_transmission_time))


def average_age_of_information(frame: pd.DataFrame) -> float:
    return float(frame['age_of_information'].mean())
