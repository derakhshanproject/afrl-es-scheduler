#!/usr/bin/env python
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description='Export summary metrics as markdown tables.')
    parser.add_argument('--metrics', default='outputs/runs/latest/metrics/averaged_metrics.csv')
    parser.add_argument('--output', default='outputs/runs/latest/tables/metric_summary.md')
    args = parser.parse_args()
    df = pd.read_csv(args.metrics)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(df.to_markdown(index=False), encoding='utf-8')
    print(f'Wrote table: {out}')


if __name__ == '__main__':
    main()
