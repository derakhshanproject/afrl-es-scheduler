from afrl_es.utils.config import load_article_configs
from afrl_es.experiments.runner import ExperimentRunner
from afrl_es.experiments.scenario import Scenario


def test_single_scenario_produces_expected_columns():
    configs = load_article_configs()
    runner = ExperimentRunner(configs)
    scenario = Scenario('node_density', 'number_of_nodes', 100, 100, 70.0, 3)
    df = runner.run_scenario(scenario, ['AFRL-ES', 'PDRL-RA'], runs=1, episodes=3)
    assert len(df) == 2
    for col in ['method', 'sweep_name', 'age_of_information', 'quality_of_service']:
        assert col in df.columns
