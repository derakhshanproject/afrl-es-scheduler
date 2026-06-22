#!/usr/bin/env python
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from afrl_es.visualization.chart_builder import build_all_charts


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate professional method-comparison charts.')
    parser.add_argument('--metrics', default='outputs/runs/latest/metrics/averaged_metrics.csv')
    parser.add_argument('--output-dir', default='outputs/runs/latest/charts')
    parser.add_argument('--formats', nargs='+', default=['png', 'pdf', 'svg'])
    args = parser.parse_args()
    summary = pd.read_csv(args.metrics)
    paths = build_all_charts(summary, Path(args.output_dir), formats=args.formats)
    print(f'Generated {len(paths)} chart files in {args.output_dir}')


if __name__ == '__main__':
    main()
