from afrl_es.metrics.age_of_information import age_of_information
from afrl_es.metrics.energy_efficiency import energy_efficiency, energy_score
from afrl_es.metrics.quality_of_service import qos_score


def test_aoi_equation_6():
    assert age_of_information(10, 4) == 6.0


def test_energy_efficiency_equation_8():
    assert abs(energy_efficiency(80, 2, 6) - 10.0) < 1e-12


def test_energy_score_equation_9():
    assert abs(energy_score(80, 4, 2, 0.6, 0.4) - (0.6*(80/4) - 0.4*2)) < 1e-12


def test_qos_modes():
    exact = qos_score(10, 50, 80, 0.4, 0.3, 0.2, mode='article_exact')
    corrected = qos_score(10, 50, 80, 0.4, 0.3, 0.2, mode='corrected')
    assert exact < corrected
