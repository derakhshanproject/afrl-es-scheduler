#!/usr/bin/env python
from __future__ import annotations
import argparse
from pathlib import Path
from afrl_es.utils.config import load_article_configs
from afrl_es.experiments.sweep_runner import run_all_sweeps
from afrl_es.utils.serialization import write_dataframe, write_json
from afrl_es.experiments.reproducibility import collect_environment_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description='Run AFRL-ES article sweeps.')
    parser.add_argument('--quick', action='store_true', help='Use 2 runs and 50 episodes for a fast smoke test.')
    parser.add_argument('--output-dir', default='outputs/runs/latest', help='Directory for output files.')
    args = parser.parse_args()
    configs = load_article_configs()
    raw, summary = run_all_sweeps(configs, quick=args.quick)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_dataframe(out / 'metrics' / 'raw_observations.csv', raw)
    write_dataframe(out / 'metrics' / 'averaged_metrics.csv', summary)
    write_dataframe(out / 'metrics' / 'averaged_metrics.xlsx', summary)
    write_json(out / 'metadata' / 'environment.json', collect_environment_manifest())
    write_json(out / 'metadata' / 'run_manifest.json', {'quick': args.quick, 'rows': len(raw), 'summary_rows': len(summary)})
    print(f'Wrote results to: {out}')


if __name__ == '__main__':
    main()
