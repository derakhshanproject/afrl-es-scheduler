from afrl_es.scheduling.priority_scorer import PriorityWeights, OverallPriorityWeights, node_priority_score, overall_priority_score, optimal_transmission_objective
import numpy as np


def test_node_priority_score_equation_1():
    w = PriorityWeights(0.35, 0.30, 0.20, 0.15)
    assert abs(node_priority_score(10, 4, 80, 0.8, w) - (0.35*10 + 0.30*4 - 0.20*80 - 0.15*0.8)) < 1e-12


def test_overall_priority_score_equation_2():
    theta = OverallPriorityWeights(0.25, 0.35, 0.25, 0.15)
    assert abs(overall_priority_score(5, 10, 4, 80, theta) - (0.25*5 + 0.35*10 + 0.25*4 - 0.15*80)) < 1e-12


def test_transmission_objective_equation_3():
    assert optimal_transmission_objective(np.array([1,2]), np.array([3,4]), np.array([5,6])) == -1.0
