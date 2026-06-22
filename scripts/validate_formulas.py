#!/usr/bin/env python
from afrl_es.scheduling.priority_scorer import PriorityWeights, OverallPriorityWeights, node_priority_score, overall_priority_score
from afrl_es.scheduling.edge_processing import estimate_processing_transmission_time
from afrl_es.learning.reward_model import RewardWeights, reward


def main() -> None:
    pw = PriorityWeights(0.35, 0.30, 0.20, 0.15)
    ow = OverallPriorityWeights(0.25, 0.35, 0.25, 0.15)
    print('S_i =', node_priority_score(10, 4, 80, 0.8, pw))
    print('Sc_i =', overall_priority_score(5, 10, 4, 80, ow))
    print('T_i =', estimate_processing_transmission_time(2, 0.2, 10, 20, 1.0, 128, 50))
    print('R_i =', reward(0.85, 10, 0.75, RewardWeights(0.4, 0.35, 0.25)))


if __name__ == '__main__':
    main()
