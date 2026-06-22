from __future__ import annotations

CHART_REGISTRY = {
    'age_of_information_by_node_density': {
        'metric': 'age_of_information',
        'sweep_name': 'node_density',
        'title': 'Age of Information by Node Density',
        'x_label': 'Number of IoT Nodes',
        'y_label': 'Average Age of Information (ms)',
    },
    'age_of_information_by_bandwidth': {
        'metric': 'age_of_information',
        'sweep_name': 'bandwidth',
        'title': 'Age of Information by Bandwidth',
        'x_label': 'Bandwidth (Mbps)',
        'y_label': 'Average Age of Information (ms)',
    },
    'information_freshness_by_data_priority': {
        'metric': 'information_freshness',
        'sweep_name': 'data_priority',
        'title': 'Information Freshness by Data Priority',
        'x_label': 'Data Priority Level',
        'y_label': 'Information Freshness (%)',
    },
    'information_freshness_by_node_density': {
        'metric': 'information_freshness',
        'sweep_name': 'node_density',
        'title': 'Information Freshness by Node Density',
        'x_label': 'Number of IoT Nodes',
        'y_label': 'Information Freshness (%)',
    },
    'energy_efficiency_by_bandwidth': {
        'metric': 'energy_efficiency',
        'sweep_name': 'bandwidth',
        'title': 'Energy Efficiency by Bandwidth',
        'x_label': 'Bandwidth (Mbps)',
        'y_label': 'Energy Efficiency (%)',
    },
    'energy_efficiency_by_data_priority': {
        'metric': 'energy_efficiency',
        'sweep_name': 'data_priority',
        'title': 'Energy Efficiency by Data Priority',
        'x_label': 'Data Priority Level',
        'y_label': 'Energy Efficiency (%)',
    },
    'quality_of_service_by_node_density': {
        'metric': 'quality_of_service',
        'sweep_name': 'node_density',
        'title': 'Quality of Service by Node Density',
        'x_label': 'Number of IoT Nodes',
        'y_label': 'Quality of Service (%)',
    },
    'quality_of_service_by_bandwidth': {
        'metric': 'quality_of_service',
        'sweep_name': 'bandwidth',
        'title': 'Quality of Service by Bandwidth',
        'x_label': 'Bandwidth (Mbps)',
        'y_label': 'Quality of Service (%)',
    },
    'quality_of_service_by_data_priority': {
        'metric': 'quality_of_service',
        'sweep_name': 'data_priority',
        'title': 'Quality of Service by Data Priority',
        'x_label': 'Data Priority Level',
        'y_label': 'Quality of Service (%)',
    },
}
