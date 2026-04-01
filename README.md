# MAPPO Learning

Priority-aware MAPPO implementation for the wireless sensing network experiments described in *Pan et al., IJCS Vol. 3 No. 1*. The repository contains the Python reference simulator, MAPPO training stack, and the evaluation utilities that produced the figures reported in the manuscript. A Chinese walkthrough is still available in [README_CN.md](README_CN.md).

> This project originates from the lightweight MAPPO template by @tinyzqh and has been extended with a custom wireless environment, evaluation pipelines, and experiment tracking tailored to the IJCS study.

---

## Overview

- **Custom environment.** `envs/env_core.py` rewrites the MAPPO environment to emulate 10 leaf nodes selecting among 3 parent relays with stochastic ETX, BO feedback, per-node capacity limits, and dynamic priority (`pi`) sampling.
- **Policy training.** `train/train.py` wraps the environment with `DummyVecEnv`, binds it to the MAPPO runner (`runner/shared/env_runner.py`), and logs checkpoints under `results/MyEnv/...`.
- **Evaluation tooling.** `EVAL.py`, `EVAL1.py`, and `custom_eval.py` reproduce the fairness (WFI), throughput, action distribution, and node-level analytics featured in the paper, exporting `.npy` traces for downstream plotting.
- **Python-first workflow for realistic training.** This repository hosts the high-fidelity Python simulator and MAPPO training scripts we used to mirror the real deployment scenario. Docker-based replay lives in a separate repo (see below) and reuses the checkpoints produced here.

---

## Repository Layout

```
mappo_learning/
├── train/train.py          # Entry point for MAPPO training
├── runner/shared/env_runner.py
├── envs/
│   ├── env_core.py         # Priority-aware WSN dynamics
│   ├── env_discrete.py     # Gym wrapper for discrete actions
│   └── env_wrappers.py     # Vectorized env helper
├── algorithms/             # MAPPO/RMAPPO implementations
├── EVAL.py / EVAL1.py      # Batch evaluation (fixed vs. dynamic priorities)
├── custom_eval.py          # Single-scenario replay with custom priors/topology
├── config.py               # Global CLI + hyperparameter parser
├── requirements.txt
├── results/                # Checkpoints and exported metrics
└── README_CN.md
```

---

## Installation

### Python environment
1. Create a Conda or venv environment (Python ≥ 3.9 recommended).
2. Install PyTorch with CUDA that matches your driver (e.g. `pip install torch==2.5.1+cu124 torchvision==0.20.1+cu124 torchaudio==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124`).
3. Install the remaining dependencies:
   ```
   pip install -r requirements.txt
   ```
   The list includes `gymnasium`, `numpy`, `scipy`, `matplotlib`, `setproctitle`, `tqdm`, etc. (Windows-style encoding in the file is expected).

### Docker validation (optional)
Docker images and runtime scripts are maintained separately in [Simulation_on_docker](https://github.com/Kongtong12/Simulation_on_docker). Use that repository when you want to replay trained agents in containerized environments; it mounts the checkpoints generated here and runs the same evaluation commands for deployment benchmarking.

---

## Quick Start (Python Simulation)

```bash
# 1) Configure hyperparameters if needed
vim config.py  # adjust PPO/MAPPO switches, threads, etc.

# 2) Launch training with custom env parameters
python -m train.train \
  --env_name MyEnv \
  --scenario_name MyEnv \
  --experiment_name check \
  --algorithm_name mappo \
  --seed 42
```

Key runtime options:
- `train/train.py` sets MAPPO defaults (shared policy, 5 rollout threads, 10 agents). Edit `get_env_params()` to sweep agent counts or reward coefficients (`alpha`, `beta`, `gamma`, `W1`, `W2`).
- Checkpoints are written to `results/<env>/<scenario>/<algo>/<experiment>/runX/models/`.
- Use `wandb` or TensorBoard via the switches exposed in `config.py` if you need remote logging.

---

## Environment Model (`envs/env_core.py`)

- **Agents and parents.** 10 leaf agents select one of 3 parent nodes each step. Actions are encoded as one-hot vectors in `env_discrete.py`.
- **Observation design.** Each agent observes concatenated BO levels, smoothed parent throughput (`xi_out`), parent-average priority, its own priority, and the previous parent selection mask, resulting in `obs_dim = 4 * parent_num + 1`.
- **Dynamics.** ETX evolves with clipped Gaussian noise, BO aggregates sending rates scaled by ETX, and parent capacities (`xi_out`) follow an AR process with noise.
- **Priorities.** `pi` values are sampled per reset (1–3) and stored to compute fairness; average parent priority is recomputed after every topology change.
- **Rewards.** `_compute_rewards` combines weighted throughput, penalties for parent switching (`switch_penalty`), and the coefficients (`alpha`, `beta`, `gamma`, `W1`, `W2`) specified through `get_env_params`.
- **Vectorization.** `env_wrappers.DummyVecEnv` batches environments for MAPPO and customizes shared observations so centralized critics see BO and priority summaries.

These mechanics align with the IJCS manuscript description: agents compete for limited relay bandwidth, priorities influence throughput fairness, and the controller learns to balance load with minimal switching.

---

## Training Workflow

1. **Configure** `config.py` (PPO epochs, entropy coef, rollout length) and `train/train.py` (env parameters, `num_agents`, checkpoint directory).
2. **Launch training** via `python -m train.train ...`. MAPPO handles value normalization, advantage estimation, and model persistence.
3. **Monitor metrics**: console logs print `average episode rewards`, and intermediate checkpoints live under `results/.../models/actor.pt` and `critic.pt`.
4. **Resume** by pointing `all_args.model_dir` to a previous run folder.

---

## Evaluation & Analysis

| Script         | Purpose | Key Outputs |
|----------------|---------|-------------|
| `EVAL.py`      | Replays a trained `actor.pt` for 500 episodes with static priorities to estimate WFI, throughput, sending-rate statistics, and action distributions. Saves `RL_WFI.npy`, `RL_throughput.npy`, `RL_ratio.npy` and prints aggregate metrics. |
| `EVAL1.py`     | Extends `EVAL.py` by randomly perturbing node priorities every 20 steps, tracking transition counts, and stress-testing policy robustness. |
| `custom_eval.py` | Allows manual injection of per-node priorities and parent assignments, then logs per-node throughput/variance, efficiency, and parent IDs for scenario studies described in the paper. |

Typical usage:

```bash
python EVAL.py --scenario_name MyEnv --num_agents 10
python EVAL1.py --scenario_name MyEnv --num_agents 10
python custom_eval.py --scenario_name MyEnv --num_agents 10 \
  --actor_path results/MyEnv/MyEnv/mappo/check/run34/models/actor.pt
```

Make sure the paths inside each script (`checkpoint = torch.load(...)`) point to the checkpoint you want to inspect.

---

## Results & Logging Artifacts

- `results/MyEnv/.../summary.log`: scalar training metrics flushed by MAPPO.
- `*.npy` files from `EVAL*.py`: sequences used to plot WFI trends, throughput time series, and throughput-to-sending-rate ratios (exactly the curves referenced in the IJCS manuscript).
- `data_record.md`: lab notebook containing experiment identifiers, reward snapshots, and notes on priority sampling ideas.

---

## Python vs. Docker Implementation

This repository focuses on the most realistic possible training setup: a Python simulator that already injects stochastic ETX, BO feedback, and priority reshuffling exactly as described in the manuscript. All algorithmic contributions (environment dynamics, MAPPO policy, evaluation) live here.

If you need the containerized replay or deployment scaffolding, visit [Simulation_on_docker](https://github.com/Kongtong12/Simulation_on_docker). That project wraps the checkpoints exported from this repo, so no Docker-specific logic is duplicated here.

---

## Citation

If you use this repository, please cite both the original lightweight MAPPO template and our IJCS article:

```
@article{pan2024mappo,
  title     = {Priority-Aware MAPPO for Wireless Sensor Networks},
  author    = {Pan, Jiasheng and co-authors},
  journal   = {International Journal of Communication Systems},
  volume    = {3},
  number    = {1},
  year      = {2024}
}

@article{qiu2024enhancing,
  title   = {Enhancing UAV Communications in Disasters: Integrating ESFM and MAPPO for Superior Performance},
  journal = {Journal of Circuits, Systems and Computers},
  year    = {2024}
}
```

---

For additional clarifications (including Docker runtime notes or manuscript excerpts), please open an issue or consult `README_CN.md` for the Chinese walkthrough.
