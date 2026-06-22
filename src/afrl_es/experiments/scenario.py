from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Scenario:
    sweep_name: str
    sweep_variable: str
    sweep_value: float | int
    number_of_nodes: int
    bandwidth_mbps: float
    data_priority_level: int | None = None


def build_scenarios(sim_cfg: dict) -> list[Scenario]:
    nodes_default = int(sim_cfg['network']['node_counts'][2])
    bandwidth_default = float(sim_cfg['network']['bandwidth_mbps'][2])
    priority_default = 3
    scenarios: list[Scenario] = []
    for n in sim_cfg['network']['node_counts']:
        scenarios.append(Scenario('node_density', 'number_of_nodes', int(n), int(n), bandwidth_default, priority_default))
    for bw in sim_cfg['network']['bandwidth_mbps']:
        scenarios.append(Scenario('bandwidth', 'bandwidth_mbps', float(bw), nodes_default, float(bw), priority_default))
    for pr in sim_cfg['network']['data_priority_levels']:
        scenarios.append(Scenario('data_priority', 'data_priority_level', int(pr), nodes_default, bandwidth_default, int(pr)))
    return scenarios
