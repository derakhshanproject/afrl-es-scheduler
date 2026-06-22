from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def apply_journal_style() -> None:
    plt.rcParams.update({
        'figure.dpi': 120,
        'savefig.dpi': 300,
        'font.size': 10,
        'axes.grid': True,
        'grid.alpha': 0.25,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })
