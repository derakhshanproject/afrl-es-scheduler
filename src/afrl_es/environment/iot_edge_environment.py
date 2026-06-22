from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from afrl_es.core.edge_server import EdgeServer
from afrl_es.core.network_state import NetworkState
from afrl_es.core.node import IoTNode
from afrl_es.core.simulation_clock import SimulationClock
from .channel_model import ChannelModel
from .energy_model import EnergyModel
from .traffic_model import TrafficModel


@dataclass(slots=True)
class IoTEdgeEnvironment:
    nodes: list[IoTNode]
    edge_server: EdgeServer
    channel_model: ChannelModel
    energy_model: EnergyModel
    traffic_model: TrafficModel
    clock: SimulationClock
    rng: np.random.Generator
    fixed_priority: int | None = None

    def observe(self) -> pd.DataFrame:
        return NetworkState(self.clock.current_time, self.nodes).to_frame()

    def step_dynamics(self) -> float:
        current_time = self.clock.tick()
        self.traffic_model.update_priorities(self.nodes, current_time, self.rng, self.fixed_priority)
        congestion = self.channel_model.update(self.nodes, self.rng)
        self.energy_model.idle_update(self.nodes, self.rng)
        return congestion

    def apply_schedule(self, scheduled_frame: pd.DataFrame) -> None:
        scheduled_ids = set(scheduled_frame.loc[scheduled_frame['scheduled'], 'node_id'].astype(int).tolist())
        scheduled_nodes = [node for node in self.nodes if node.node_id in scheduled_ids]
        self.edge_server.process_scheduled_nodes(scheduled_nodes, self.clock.current_time)
        self.energy_model.transmission_update(scheduled_nodes)
        for node in scheduled_nodes:
            node.last_transmission_time = self.clock.current_time
            node.waiting_time_ms = max(0.0, node.waiting_time_ms * 0.25)
