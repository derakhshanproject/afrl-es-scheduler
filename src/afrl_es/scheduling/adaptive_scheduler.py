from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .priority_scorer import PriorityWeights, OverallPriorityWeights, score_frame
from .eligibility_checker import EligibilityChecker
from .transmission_policy import TransmissionPolicy


@dataclass(slots=True)
class AdaptiveScheduler:
    priority_weights: PriorityWeights
    overall_weights: OverallPriorityWeights
    eligibility_checker: EligibilityChecker
    transmission_policy: TransmissionPolicy

    def schedule(self, observation_frame: pd.DataFrame) -> pd.DataFrame:
        scored = score_frame(observation_frame, self.priority_weights, self.overall_weights)
        eligible = self.eligibility_checker.mark_eligible(scored)
        return self.transmission_policy.select(eligible)

    def update_weights(self, new_weights: PriorityWeights) -> None:
        self.priority_weights = new_weights
