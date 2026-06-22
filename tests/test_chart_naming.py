from afrl_es.visualization.naming import artifact_name


def test_no_figure_number_in_artifact_name():
    name = artifact_name('age_of_information', 'node_density')
    assert name == 'age_of_information__by__node_density__method_comparison.png'
    assert 'fig' not in name.lower()
