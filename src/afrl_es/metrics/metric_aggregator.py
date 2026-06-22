from __future__ import annotations
import pandas as pd
from .age_of_information import average_age_of_information
from .information_freshness import freshness_percentage
from .energy_efficiency import energy_efficiency_percentage
from .quality_of_service import qos_percentage


def aggregate_metrics(frame: pd.DataFrame) -> dict[str, float]:
    scheduled = frame[frame['scheduled']] if 'scheduled' in frame else frame
    target = scheduled if len(scheduled) else frame
    return {
        'age_of_information': average_age_of_information(target),
        'information_freshness': freshness_percentage(target),
        'energy_efficiency': energy_efficiency_percentage(target),
        'quality_of_service': qos_percentage(target),
        'scheduled_ratio': float(frame['scheduled'].mean()) if 'scheduled' in frame else 1.0,
        'eligible_ratio': float(frame['eligible'].mean()) if 'eligible' in frame else 1.0,
    }


def summarize_runs(results: pd.DataFrame) -> pd.DataFrame:
    group_cols = ['method', 'sweep_name', 'sweep_variable', 'sweep_value']
    metric_cols = ['age_of_information', 'information_freshness', 'energy_efficiency', 'quality_of_service', 'scheduled_ratio', 'eligible_ratio']
    summary = results.groupby(group_cols, as_index=False)[metric_cols].agg(['mean', 'std'])
    summary.columns = ['_'.join(c).rstrip('_') for c in summary.columns.to_flat_index()]
    summary = summary.rename(columns={
        'method_': 'method', 'sweep_name_': 'sweep_name', 'sweep_variable_': 'sweep_variable', 'sweep_value_': 'sweep_value'
    })
    return summary
