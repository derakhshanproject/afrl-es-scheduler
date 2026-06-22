# Implementation Notes

This document records how the article was translated into code.

## Method mapping

| Article concept | Code location |
|---|---|
| Feature collection | `core/node.py`, `core/network_state.py` |
| Priority score | `scheduling/priority_scorer.py` |
| Eligibility check | `scheduling/eligibility_checker.py` |
| Scheduling | `scheduling/adaptive_scheduler.py` |
| Edge processing | `core/edge_server.py`, `scheduling/edge_processing.py` |
| RL reward | `learning/reward_model.py` |
| RL weight update | `learning/weight_adapter.py` |
| AoI metric | `metrics/age_of_information.py` |
| Energy metric | `metrics/energy_efficiency.py` |
| QoS metric | `metrics/quality_of_service.py` |
| Experiment sweeps | `experiments/sweep_runner.py` |
| Chart registry | `visualization/chart_registry.py` |

## Why baselines are calibrated

The article names the baselines but does not provide enough details to reimplement them exactly. The project therefore keeps baseline behavior configurable in YAML. This makes the assumption visible.
