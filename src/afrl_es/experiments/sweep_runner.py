from __future__ import annotations
import pandas as pd
from afrl_es.experiments.scenario import build_scenarios
from afrl_es.experiments.runner import ExperimentRunner
from afrl_es.metrics.metric_aggregator import summarize_runs


def run_all_sweeps(configs: dict, quick: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    sim = configs['simulation']
    method_names = list(configs['reference_methods']['methods'].keys())
    runs = 2 if quick else int(sim['runtime']['independent_runs'])
    episodes = 5 if quick else int(sim['runtime']['training_episodes'])
    runner = ExperimentRunner(configs)
    frames = []
    for scenario in build_scenarios(sim):
        frames.append(runner.run_scenario(scenario, method_names, runs=runs, episodes=episodes))
    raw = pd.concat(frames, ignore_index=True)
    summary = summarize_runs(raw)
    return raw, summary
