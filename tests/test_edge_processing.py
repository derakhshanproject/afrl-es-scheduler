from afrl_es.scheduling.edge_processing import estimate_processing_transmission_time


def test_edge_processing_equation_4_positive():
    value = estimate_processing_transmission_time(2.0, 0.2, 10.0, 20.0, 1.0, 128.0, 50.0)
    expected = 2.0 * ((0.2 + 10.0) / 20.0) + 128.0 / 50.0
    assert abs(value - expected) < 1e-12
