from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(fig: plt.Figure, output_dir: Path, filename_stem: str, formats: list[str]) -> list[Path]:
    paths = []
    for ext in formats:
        subdir = output_dir / ext
        subdir.mkdir(parents=True, exist_ok=True)
        path = subdir / f"{filename_stem}.{ext}"
        fig.savefig(path, bbox_inches='tight')
        paths.append(path)
    return paths
