# AFRL-ES Scheduler

**Adaptive Reinforcement Learning-Based Edge Scheduling for Age of Information in IoT**

This repository implements a reproducible, article-faithful research simulator for the proposed **AFRL-ES** method. The project follows the article configuration, formulas, metrics, comparison methods, and evaluation variables as closely as possible while keeping the code clean, testable, and reusable.

The implementation is written in Python, but the configuration explicitly records the article's reported MATLAB-based simulation environment. The goal is not to build a vague reinforcement learning demo. The goal is to build a structured research codebase that resembles the article's method: IoT feature collection, priority scoring, adaptive scheduling, edge processing, lightweight reinforcement-learning weight adjustment, and metric-based evaluation.

---

## 1. What this project implements

The article proposes **AFRL-ES**, an adaptive scheduler for IoT edge networks. The scheduler is designed to improve:

1. **Age of Information (AoI)**
2. **Information freshness**
3. **Energy efficiency**
4. **Quality of Service (QoS)**

The project models a dense IoT edge environment where heterogeneous nodes periodically generate data. Each node has a dynamic state:

- Age of Information
- remaining energy
- data priority
- communication quality
- bandwidth
- processing cost
- processing delay
- packet size
- power consumption
- last transmission time
- waiting time

The scheduler uses these values to rank nodes and decide which nodes should transmit data during each scheduling cycle.

---

## 2. Important design decision: this is lightweight RL, not DQN

The article discusses Q-learning and Deep Q-Networks, but the proposed AFRL-ES update is defined as a lightweight coefficient update:

```text
w_new = w_old + alpha * (R - P)
```

So this repository does **not** pretend that the proposed method is a full DQN. It implements the article's actual mechanism: dynamic adjustment of scheduling weights using reward prediction error.

This is important for academic honesty. A DQN implementation would be a different method unless the article provides the full neural-network architecture, replay buffer, state-action design, target network, optimizer, and hyperparameters.

---

## 3. Repository structure

```text
afrl_es_scheduler/
│
├── configs/
│   ├── article/
│   │   ├── simulation.yaml
│   │   ├── afrl_es.yaml
│   │   ├── reference_methods.yaml
│   │   └── evaluation.yaml
│   │
│   ├── sweeps/
│   │   ├── node_density.yaml
│   │   ├── bandwidth.yaml
│   │   └── data_priority.yaml
│   │
│   └── plotting/
│       └── journal_style.yaml
│
├── src/
│   └── afrl_es/
│       ├── core/
│       ├── environment/
│       ├── scheduling/
│       ├── learning/
│       ├── metrics/
│       ├── reference_methods/
│       ├── experiments/
│       ├── visualization/
│       └── utils/
│
├── scripts/
│   ├── run_all_sweeps.py
│   ├── generate_charts.py
│   ├── reproduce_article_results.py
│   ├── export_metric_tables.py
│   └── validate_formulas.py
│
├── tests/
├── outputs/
├── data/
├── docs/
├── README.md
├── pyproject.toml
├── requirements.txt
└── environment.yml
```

---

## 4. Article-faithful configuration

The main simulation values are stored in:

```text
configs/article/simulation.yaml
```

The article-based values are:

| Parameter | Value |
|---|---:|
| Environment | IoT Edge Computing |
| Number of nodes | 100, 200, 300, 400, 500 |
| Bandwidth | 50, 60, 70, 80, 90 Mbps |
| Data priority levels | 1, 2, 3, 4, 5 |
| Learning rate alpha | 0.1 |
| Discount factor gamma | 0.9 |
| Energy threshold | 20% of initial energy |
| QoS threshold | 0.8 |
| Training episodes | 1000 |
| Independent runs | 10 |
| Traffic model | Periodic data generation |
| Node mobility | Static nodes |
| Communication quality | Dynamic |
| Energy level | Dynamic |
| Dataset type | Simulation-based |

The project keeps these values in YAML so that the configuration is transparent and easy to cite or modify.

---

## 5. Core mathematical formulation

### 5.1 Node priority score

Implemented in:

```text
src/afrl_es/scheduling/priority_scorer.py
```

Formula:

```text
S_i = w1 * AoI_i + w2 * Pr_i - w3 * Er_i - w4 * Qc_i
```

Meaning:

- `AoI_i`: Age of Information of node `i`
- `Pr_i`: data priority
- `Er_i`: remaining energy
- `Qc_i`: communication quality
- `w1, w2, w3, w4`: adaptive scheduling weights

Higher AoI and higher data priority increase the scheduling score. Lower energy and poor communication quality reduce scheduling priority to protect the network.

### 5.2 Overall priority score

```text
Sc_i = theta1 * TL_i + theta2 * AoI_i + theta3 * Pr_i - theta4 * Er_i
```

This score adds the time since last transmission to improve fairness among nodes.

### 5.3 Optimal transmission objective

```text
T_opt = argmin_T sum_i(AoI_i + Pr_i - Er_i)
```

The implementation uses this as an objective signal. The scheduler ranks nodes by priority and selects eligible nodes under energy and link-quality constraints.

### 5.4 Edge processing and transmission time

```text
T_i = W_{i-1} * ((C_i + D_i) / R_i) + epsilon_i * (L_i / B_i)
```

Where:

- `W_{i-1}`: waiting time of previous packet
- `C_i`: processing cost
- `D_i`: processing delay
- `R_i`: transmission rate
- `epsilon_i`: packet importance weight
- `L_i`: packet size
- `B_i`: available bandwidth

Implemented in:

```text
src/afrl_es/scheduling/edge_processing.py
```

### 5.5 Reinforcement-learning state

```text
s_t = {AoI_i, Er_i, Pr_i, Qc_i}
```

Implemented in:

```text
src/afrl_es/learning/state_encoder.py
```

### 5.6 Reinforcement-learning action

```text
a_t = {w1, w2, w3, w4}
```

The action is not a task-offloading decision. The action is the adjustment of scheduling weights.

### 5.7 Reward function

```text
R_i = lambda1 * QoS - lambda2 * AoI + lambda3 * Ef_i
```

Implemented in:

```text
src/afrl_es/learning/reward_model.py
```

### 5.8 Weight update

```text
w_i_new = w_i_old + alpha * (R_i - P_i)
```

Implemented in:

```text
src/afrl_es/learning/weight_adapter.py
```

---

## 6. Evaluation metrics

The project computes the article metrics in separate modules.

### 6.1 Age of Information

```text
AoI_i(t) = t - t_i,last
```

File:

```text
src/afrl_es/metrics/age_of_information.py
```

### 6.2 Information freshness

Article score:

```text
S_AoI_i = gamma1 * AoI_i + gamma2 * TL - gamma3 * Er_i
```

The raw equation is an AoI-risk score. For charting, the project also reports a bounded freshness percentage so the plots are easier to interpret.

File:

```text
src/afrl_es/metrics/information_freshness.py
```

### 6.3 Energy efficiency

```text
Ef_i = Er_i / (P_i + C_i)
```

Energy score:

```text
S_En_i = delta1 * (Er_i / C_i) - delta2 * P_i
```

File:

```text
src/afrl_es/metrics/energy_efficiency.py
```

### 6.4 Quality of Service

Article formula:

```text
S_QoS_i = rho1 * (1 / D_i) - rho2 * B_i - rho3 * Er_i
```

The article-exact mode is the default. Because this formula penalizes bandwidth and energy, the project also exposes a corrected engineering mode:

```text
S_QoS_i = rho1 * (1 / D_i) + rho2 * B_i + rho3 * Er_i
```

To change it, edit:

```text
configs/article/evaluation.yaml
```

Set:

```yaml
qos:
  formula_mode: corrected
```

---

## 7. Reference methods

The article compares AFRL-ES with:

- PDRL-RA
- DRL-MEC
- DT-AoI
- MA-AoI

The article names these methods but does not provide complete implementation details for all baselines. This repository handles that limitation transparently.

The proposed method is implemented mechanistically. The reference methods are implemented as calibrated article-reproduction surrogates, controlled from:

```text
configs/article/reference_methods.yaml
```

This is the cleanest academic approach because it avoids inventing hidden hyperparameters that are not present in the article.

---

## 8. Professional chart naming

The project does **not** use manuscript figure numbers in filenames.

Bad style:

```text
fig3_aoi_nodes.png
figure_4_bandwidth.png
```

Professional style used here:

```text
age_of_information__by__node_density__method_comparison.png
age_of_information__by__bandwidth__method_comparison.png
information_freshness__by__data_priority__method_comparison.png
information_freshness__by__node_density__method_comparison.png
energy_efficiency__by__bandwidth__method_comparison.png
energy_efficiency__by__data_priority__method_comparison.png
quality_of_service__by__node_density__method_comparison.png
quality_of_service__by__bandwidth__method_comparison.png
quality_of_service__by__data_priority__method_comparison.png
```

This is better because manuscript figure numbers can change during revision, but experiment meaning should remain stable.

---

## 9. Installation

### 9.1 Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

Linux or macOS:

```bash
source .venv/bin/activate
```

### 9.2 Install dependencies

```bash
pip install -r requirements.txt
```

### 9.3 Install the project in editable mode

```bash
pip install -e .
```

---

## 10. Validate formulas

Run:

```bash
python scripts/validate_formulas.py
```

This prints values for the main equations:

- Equation 1 priority score
- Equation 2 overall priority score
- Equation 4 processing/transmission time
- reward function

---

## 11. Run a quick smoke test

Use quick mode first:

```bash
python scripts/reproduce_article_results.py --quick --output-dir outputs/runs/quick_test
```

Quick mode uses:

- 2 independent runs
- 5 episodes

This is not article-exact runtime. It is for checking that the project works.

Generated files:

```text
outputs/runs/quick_test/
├── metrics/
│   ├── raw_observations.csv
│   ├── averaged_metrics.csv
│   └── averaged_metrics.xlsx
├── charts/
│   ├── png/
│   ├── pdf/
│   └── svg/
└── metadata/
    ├── environment.json
    └── run_manifest.json
```

---

## 12. Run the full article-scale experiment

Run:

```bash
python scripts/reproduce_article_results.py --output-dir outputs/runs/article_reproduction
```

This uses the article configuration:

- 1000 episodes
- 10 independent runs
- all node-density values
- all bandwidth values
- all data-priority levels
- AFRL-ES plus all reference methods

This will take longer than quick mode.

---

## 13. Run only the sweeps without charts

```bash
python scripts/run_all_sweeps.py --output-dir outputs/runs/latest
```

Fast version:

```bash
python scripts/run_all_sweeps.py --quick --output-dir outputs/runs/latest
```

---

## 14. Generate charts from existing metrics

```bash
python scripts/generate_charts.py \
  --metrics outputs/runs/latest/metrics/averaged_metrics.csv \
  --output-dir outputs/runs/latest/charts
```

Export only PNG:

```bash
python scripts/generate_charts.py \
  --metrics outputs/runs/latest/metrics/averaged_metrics.csv \
  --output-dir outputs/runs/latest/charts \
  --formats png
```

---

## 15. Export markdown metric table

```bash
python scripts/export_metric_tables.py \
  --metrics outputs/runs/latest/metrics/averaged_metrics.csv \
  --output outputs/runs/latest/tables/metric_summary.md
```

---

## 16. Run tests

```bash
pytest
```

The tests check:

- Equation 1
- Equation 2
- Equation 3
- Equation 4
- Equation 6
- Equation 8
- Equation 9
- QoS formula modes
- RL weight-update bounds
- sweep runner output columns
- chart filename policy

---

## 17. How to modify experiments

### Change number of nodes

Edit:

```text
configs/article/simulation.yaml
```

```yaml
network:
  node_counts: [100, 200, 300, 400, 500]
```

### Change bandwidth

```yaml
network:
  bandwidth_mbps: [50, 60, 70, 80, 90]
```

### Change priority levels

```yaml
network:
  data_priority_levels: [1, 2, 3, 4, 5]
```

### Change number of episodes

```yaml
runtime:
  training_episodes: 1000
```

### Change independent runs

```yaml
runtime:
  independent_runs: 10
```

### Change learning rate

```yaml
learning:
  alpha: 0.10
```

File:

```text
configs/article/afrl_es.yaml
```

---

## 18. How the scheduler works internally

Each episode follows this process:

1. Advance simulation clock.
2. Update traffic priorities.
3. Update communication quality.
4. Update available bandwidth.
5. Update node energy.
6. Collect node observations.
7. Calculate Equation 1 node score.
8. Calculate Equation 2 overall score.
9. Combine both scores.
10. Check energy threshold.
11. Check link-quality threshold.
12. Sort eligible nodes.
13. Schedule top-ranked nodes.
14. Process selected data at edge server.
15. Update node energy and last transmission time.
16. Compute AoI, freshness, energy, and QoS metrics.
17. Compute reward.
18. Update AFRL-ES weights using the lightweight RL rule.

---

## 19. Output interpretation

### Age of Information

Lower is better. The article expects AFRL-ES to keep lower AoI than reference methods.

### Information freshness

Higher is better. The project reports this as a percentage-like score for easy charting.

### Energy efficiency

Higher is better. AFRL-ES should maintain stronger energy efficiency because it avoids unnecessary transmissions and uses edge processing.

### Quality of Service

Higher is better. QoS improves when delay is low, communication quality is high, energy remains stable, and bandwidth is used effectively.

---

## 20. Known article limitations handled in code

### 20.1 Baseline implementation gap

The article does not provide complete source-level details for PDRL-RA, DRL-MEC, DT-AoI, and MA-AoI. The project therefore uses configurable surrogate methods for article-style reproduction.

### 20.2 QoS formula sign issue

The article's QoS equation subtracts bandwidth and energy. This is kept in `article_exact` mode. A corrected mode is also available.

### 20.3 Bandwidth range conflict

The article table reports 50--90 Mbps. One plot appears to use a 10--50 Mbps visual range. The project stores both:

```yaml
bandwidth_mbps: [50, 60, 70, 80, 90]
legacy_bandwidth_mbps: [10, 20, 30, 40, 50]
```

The default uses the table values.

---

## 21. How to cite this code in an article

Suggested text:

```text
The simulation code implements the AFRL-ES scheduling framework using the same configuration, evaluation metrics, and parameter ranges described in the article. The implementation includes the proposed adaptive priority scheduler, lightweight reinforcement-learning weight update, synthetic IoT edge environment, reference-method reproduction layer, and scripts for generating all evaluation tables and charts.
```

---

## 22. Development notes

The project is designed for extension. Useful future additions include:

- real IoT trace ingestion
- full MATLAB port
- actual DQN baseline implementation
- NS-3 or OMNeT++ network simulator bridge
- edge-server placement models
- trust-aware RL feedback
- adversarial false-feedback simulation
- confidence intervals on charts

---

## 23. Minimal command sequence

```bash
pip install -r requirements.txt
pip install -e .
pytest
python scripts/reproduce_article_results.py --quick --output-dir outputs/runs/quick_test
```

For full article-scale reproduction:

```bash
python scripts/reproduce_article_results.py --output-dir outputs/runs/article_reproduction
```
