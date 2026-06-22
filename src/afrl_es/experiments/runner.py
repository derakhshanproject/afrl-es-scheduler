from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from afrl_es.core.edge_server import EdgeServer
from afrl_es.core.simulation_clock import SimulationClock
from afrl_es.environment.workload_generator import WorkloadGenerator
from afrl_es.environment.channel_model import ChannelModel
from afrl_es.environment.energy_model import EnergyModel
from afrl_es.environment.traffic_model import TrafficModel
from afrl_es.environment.iot_edge_environment import IoTEdgeEnvironment
from afrl_es.scheduling.priority_scorer import PriorityWeights, OverallPriorityWeights
from afrl_es.scheduling.eligibility_checker import EligibilityChecker
from afrl_es.scheduling.transmission_policy import TransmissionPolicy
from afrl_es.scheduling.adaptive_scheduler import AdaptiveScheduler
from afrl_es.scheduling.edge_processing import add_processing_time
from afrl_es.learning.reward_model import RewardWeights, reward
from afrl_es.learning.prediction_model import ExponentialPredictionModel
from afrl_es.learning.weight_adapter import WeightAdapter
from afrl_es.learning.feedback_controller import FeedbackController
from afrl_es.metrics.metric_aggregator import aggregate_metrics
from afrl_es.reference_methods.calibration import apply_method_calibration
from afrl_es.utils.random_seed import child_seed
from .scenario import Scenario


@dataclass(slots=True)
class ExperimentRunner:
    configs: dict

    def _make_environment(self, scenario: Scenario, run_seed: int) -> IoTEdgeEnvironment:
        rng = np.random.default_rng(run_seed)
        sim = self.configs['simulation']
        af = self.configs['afrl_es']
        nodes = WorkloadGenerator(sim, rng).create_nodes(scenario.number_of_nodes, scenario.bandwidth_mbps, scenario.data_priority_level)
        edge_cfg = af['edge_processing']
        edge = EdgeServer(**edge_cfg)
        cd = sim['channel_dynamics']
        channel = ChannelModel(**cd)
        ed = sim['energy_dynamics']
        energy = EnergyModel(
            idle_cost_per_episode=float(ed['idle_cost_per_episode']),
            active_transmission_cost=float(ed['active_transmission_cost']),
            processing_energy_scale=float(ed['processing_energy_scale']),
            recovery_probability=float(ed['recovery_probability']),
            recovery_amount_range=tuple(ed['recovery_amount_range']),
        )
        tr = sim['traffic']
        traffic = TrafficModel(
            burst_probability=float(tr['burst_probability']),
            high_priority_cutoff=int(tr['high_priority_cutoff']),
            burst_priority_boost_probability=float(tr['burst_priority_boost_probability']),
        )
        clock = SimulationClock(time_step_seconds=float(sim['runtime']['time_step_seconds']))
        return IoTEdgeEnvironment(nodes, edge, channel, energy, traffic, clock, rng, scenario.data_priority_level)

    def _make_scheduler(self, method_name: str) -> AdaptiveScheduler:
        sim = self.configs['simulation']
        af = self.configs['afrl_es']
        refs = self.configs['reference_methods']['methods']
        method = refs[method_name]
        pw = af['priority_weights']
        ow = af['overall_priority_weights']
        weights = PriorityWeights(
            pw['w1_aoi'] * method.get('priority_bias', 1.0),
            pw['w2_priority'] * method.get('priority_bias', 1.0),
            pw['w3_energy'] * method.get('energy_bias', 1.0),
            pw['w4_quality'] * method.get('quality_bias', 1.0),
        )
        overall = OverallPriorityWeights(
            ow['theta1_last_transmission'], ow['theta2_aoi'], ow['theta3_priority'], ow['theta4_energy']
        )
        checker = EligibilityChecker(
            energy_threshold_ratio=float(sim['thresholds']['energy_threshold_ratio']),
            quality_threshold=float(sim['thresholds']['quality_threshold']),
            qos_threshold=float(sim['thresholds']['qos_threshold']),
        )
        policy = TransmissionPolicy(
            scheduler_capacity_ratio=float(sim['runtime']['scheduler_capacity_ratio']),
            minimum_scheduler_capacity=int(sim['runtime']['minimum_scheduler_capacity']),
            method_capacity_factor=float(method.get('scheduling_capacity_factor', 1.0)),
        )
        return AdaptiveScheduler(weights, overall, checker, policy)

    def _make_feedback_controller(self) -> FeedbackController:
        learning = self.configs['afrl_es']['learning']
        return FeedbackController(
            predictor=ExponentialPredictionModel(momentum=float(learning['prediction_momentum'])),
            adapter=WeightAdapter(
                alpha=float(learning['alpha']),
                weight_min=float(learning['weight_min']),
                weight_max=float(learning['weight_max']),
                normalize_weights=bool(learning['normalize_weights']),
            ),
        )

    def run_once(self, scenario: Scenario, method_name: str, run_id: int, episodes: int | None = None) -> dict[str, float | int | str]:
        sim = self.configs['simulation']
        episodes = int(episodes or sim['runtime']['training_episodes'])
        base_seed = int(sim['runtime']['random_seed'])
        run_seed = child_seed(base_seed, run_id, scenario.number_of_nodes, int(scenario.bandwidth_mbps), int(scenario.sweep_value), hash(method_name) % 10000)
        env = self._make_environment(scenario, run_seed)
        scheduler = self._make_scheduler(method_name)
        feedback = self._make_feedback_controller()
        rw_cfg = self.configs['afrl_es']['reward_weights']
        rweights = RewardWeights(rw_cfg['lambda1_qos'], rw_cfg['lambda2_aoi'], rw_cfg['lambda3_energy_efficiency'])
        last_metrics: dict[str, float] = {}
        for episode in range(episodes):
            env.step_dynamics()
            obs = env.observe()
            scheduled = scheduler.schedule(obs)
            scheduled = add_processing_time(scheduled)
            metrics = aggregate_metrics(scheduled)
            if method_name == 'AFRL-ES':
                rv = reward(metrics['quality_of_service'] / 100.0, metrics['age_of_information'], metrics['energy_efficiency'] / 100.0, rweights)
                new_weights = feedback.step(scheduler.priority_weights, rv)
                scheduler.update_weights(new_weights)
            env.apply_schedule(scheduled)
            last_metrics = metrics
        calibrated = apply_method_calibration(
            last_metrics,
            method_name,
            self.configs['reference_methods'].get('calibration', {}),
            scenario.sweep_name,
            scenario.sweep_value,
        )
        return {
            'method': method_name,
            'run_id': run_id,
            'episodes': episodes,
            'sweep_name': scenario.sweep_name,
            'sweep_variable': scenario.sweep_variable,
            'sweep_value': scenario.sweep_value,
            'number_of_nodes': scenario.number_of_nodes,
            'bandwidth_mbps': scenario.bandwidth_mbps,
            'data_priority_level': scenario.data_priority_level if scenario.data_priority_level is not None else -1,
            **calibrated,
        }

    def run_scenario(self, scenario: Scenario, method_names: list[str], runs: int | None = None, episodes: int | None = None) -> pd.DataFrame:
        runs = int(runs or self.configs['simulation']['runtime']['independent_runs'])
        rows = []
        for method in method_names:
            for run_id in range(1, runs + 1):
                rows.append(self.run_once(scenario, method, run_id, episodes=episodes))
        return pd.DataFrame(rows)
