from afrl_es.scheduling.priority_scorer import PriorityWeights
from afrl_es.learning.weight_adapter import WeightAdapter


def test_weight_update_bounds_and_normalization():
    weights = PriorityWeights(0.35, 0.30, 0.20, 0.15)
    adapter = WeightAdapter(alpha=0.1, weight_min=0.01, weight_max=1.0, normalize_weights=True)
    new_weights = adapter.update(weights, reward_value=2.0, predicted_value=1.0)
    arr = new_weights.as_array()
    assert abs(arr.sum() - 1.0) < 1e-12
    assert (arr >= 0.01).all()
