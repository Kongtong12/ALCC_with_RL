import sys
import os
import socket
import setproctitle
import numpy as np
from pathlib import Path
import torch
from envs.env_discrete import DiscreteActionEnv
from algorithms.algorithm.r_actor_critic import R_Actor

def _t2n(x):
    return x.detach().cpu().numpy()

def parse_args(args, parser):
    parser.add_argument("--scenario_name", type=str, default="MyEnv", help="Which scenario to run on")
    parser.add_argument("--num_landmarks", type=int, default=3)
    parser.add_argument("--num_agents", type=int, default=2, help="number of players")

    all_args = parser.parse_known_args(args)[0]

    return all_args


# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "."))

# Append the parent directory to sys.path, otherwise the following import will fail
sys.path.append(parent_dir)

from config import get_config

checkpoint = torch.load(r'D:\learning\reinforcement_learning\light_mappo\results\MyEnv\MyEnv\mappo\check\run27\models\actor.pt', map_location=torch.device('cuda'))
if isinstance(checkpoint, dict):
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint

parser = get_config()
all_args = parse_args(sys.argv[1:], parser)

# 下面修改默认的参数
all_args.share_policy = True
all_args.num_agents = 10
'''all_args.algorithm_name = "rmappo"
all_args.use_recurrent_policy = True'''
all_args.num_env_steps = 3* 1e5
all_args.use_eval = True
# 下面是一些参数的定义
episode_length = all_args.episode_length
n_rollout_threads = 1
num_agents = 10
recurrent_N = all_args.recurrent_N
hidden_size = all_args.hidden_size

env = DiscreteActionEnv()
env.seed(all_args.seed)
obs = env.reset()

actor = R_Actor(all_args, env.observation_space[0], env.action_space[0], device=torch.device('cuda'))
actor.load_state_dict(state_dict)





eval_episode_rewards = []
rnn_states = np.zeros((episode_length + 1, n_rollout_threads, num_agents, recurrent_N, hidden_size),dtype=np.float32).shape[2:]
eval_rnn_states = np.zeros((1, *rnn_states),dtype=np.float32)
eval_masks = np.ones((n_rollout_threads, num_agents, 1), dtype=np.float32)
# 以下是一个episode的循环
for step in range(episode_length):
    actions, _,rnn_states = actor(obs, eval_rnn_states, eval_masks, deterministic=True,)
    actions = _t2n(actions)
    print(actions)
