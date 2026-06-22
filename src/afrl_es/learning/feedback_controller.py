from __future__ import annotations
from dataclasses import dataclass
from afrl_es.scheduling.priority_scorer import PriorityWeights
from .prediction_model import ExponentialPredictionModel
from .weight_adapter import WeightAdapter


@dataclass(slots=True)
class FeedbackController:
    predictor: ExponentialPredictionModel
    adapter: WeightAdapter

    def step(self, weights: PriorityWeights, reward_value: float) -> PriorityWeights:
        predicted = self.predictor.predict()
        new_weights = self.adapter.update(weights, reward_value, predicted)
        self.predictor.update(reward_value)
        return new_weights
