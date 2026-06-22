from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from .chart_registry import CHART_REGISTRY
from .naming import artifact_name
from .style_manager import apply_journal_style
from .export_manager import save_figure


def build_chart(summary: pd.DataFrame, chart_key: str, output_dir: Path, formats: list[str] | None = None) -> list[Path]:
    if chart_key not in CHART_REGISTRY:
        raise KeyError(f"Unknown chart key: {chart_key}")
    cfg = CHART_REGISTRY[chart_key]
    metric = cfg['metric']
    sweep_name = cfg['sweep_name']
    formats = formats or ['png', 'pdf', 'svg']
    apply_journal_style()
    data = summary[summary['sweep_name'] == sweep_name].copy()
    y_col = f'{metric}_mean'
    if y_col not in data.columns:
        raise KeyError(f"Missing metric column in summary: {y_col}")
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for method, group in data.groupby('method'):
        group = group.sort_values('sweep_value')
        ax.plot(group['sweep_value'], group[y_col], marker='o', linewidth=2, markersize=5, label=method)
    ax.set_title(cfg['title'])
    ax.set_xlabel(cfg['x_label'])
    ax.set_ylabel(cfg['y_label'])
    ax.legend(frameon=True)
    stem = artifact_name(metric, sweep_name, extension='').rstrip('.')
    paths = save_figure(fig, output_dir, stem, formats)
    plt.close(fig)
    return paths


def build_all_charts(summary: pd.DataFrame, output_dir: Path, formats: list[str] | None = None) -> list[Path]:
    paths: list[Path] = []
    for key in CHART_REGISTRY:
        paths.extend(build_chart(summary, key, output_dir, formats=formats))
    return paths
