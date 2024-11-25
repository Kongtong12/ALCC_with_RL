import sys
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # 为了防止OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
import socket
import setproctitle
import numpy as np
from pathlib import Path
import torch
from envs.env_discrete import DiscreteActionEnv
from algorithms.algorithm.r_actor_critic import R_Actor
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def _t2n(x):
    return x.detach().cpu().numpy()

def parse_args(args, parser):
    parser.add_argument("--scenario_name", type=str, default="MyEnv", help="Which scenario to run on")
    parser.add_argument("--num_landmarks", type=int, default=3)
    parser.add_argument("--num_agents", type=int, default=2, help="number of players")

    all_args = parser.parse_known_args(args)[0]

    return all_args

def get_env_params(agent_num = 10, alpha=-1.0, beta=1.0, gamma=0.2, W1=0.4, W2=0.6):
    params = {
        'agent_num': agent_num,  # 智能体数量
        'alpha': alpha,  # 奖励参数 alpha
        'beta': beta,    # 奖励参数 beta
        'gamma': gamma,  # 奖励参数 gamma
        'W1': W1,        # ETX 的权重
        'W2': W2         # BO 的权重
    }
    return params

params = get_env_params(agent_num = 10, alpha=-1.0, beta=1.0, gamma=0.2, W1=0.4, W2=0.6)

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "."))

# Append the parent directory to sys.path, otherwise the following import will fail
sys.path.append(parent_dir)

from config import get_config

# checkpoint = torch.load(r'results\MyEnv\MyEnv\mappo\check\run36\models\actor.pt', map_location=torch.device('cuda'))
checkpoint = torch.load(r'results\MyEnv\MyEnv\mappo\check\run54\models\actor.pt', map_location=torch.device('cuda'))
# laptop段41,43较好
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
parent_num = 3

env = DiscreteActionEnv(**params)

actor = R_Actor(all_args, env.observation_space[0], env.action_space[0], device=torch.device('cuda'))
actor.load_state_dict(state_dict)





eval_episode_rewards = []
rnn_states = np.zeros((episode_length + 1, n_rollout_threads, num_agents, recurrent_N, hidden_size),dtype=np.float32).shape[2:]
eval_rnn_states = np.zeros((1, *rnn_states),dtype=np.float32)
eval_masks = np.ones((n_rollout_threads, num_agents, 1), dtype=np.float32)

epoch_rewards = []
epoch_rewards_1 = []
epoch_rewards_2 = []
epoch_rewards_3 = []
total_bo = []
for epoch in range(50):
    obs = env.reset()
    total_rewards = 0
    total_rewards_1 = 0
    total_rewards_2 = 0
    total_rewards_3 = 0
    # 以下是一个episode的循环
    for step in range(episode_length):
        actions, _,rnn_states = actor(obs, eval_rnn_states, eval_masks, deterministic=False,)
        actions = _t2n(actions)
        actions_env = np.squeeze(np.eye(env.action_space[0].n)[actions], 1)
        obs, rewards, dones, infos = env.step(actions_env)
        rewards_1, rewards_2, rewards_3 = env.get_reward()
        if step:
            total_bo.append(obs[0][parent_num:2*parent_num])
        total_rewards += np.average(rewards)
        total_rewards_1 += np.average(rewards_1)
        total_rewards_2 += np.average(rewards_2)
        total_rewards_3 += np.average(rewards_3)
        '''if total_rewards < -1000:
            print("total_rewards:", total_rewards)'''
    print(f"Epoch {epoch + 1}/{50}, Average Reward: {total_rewards:.4f}")
    epoch_rewards.append(total_rewards)
    epoch_rewards_1.append(total_rewards_1)
    epoch_rewards_2.append(total_rewards_2)
    epoch_rewards_3.append(total_rewards_3)
print("average_rewards:", np.average(epoch_rewards))
print("average_rewards_1:", np.average(epoch_rewards_1))
print("average_rewards_2:", np.average(epoch_rewards_2))
print("average_rewards_3:", np.average(epoch_rewards_3))
# 使用KDE绘制平滑的密度分布曲线
flat_bo = np.array(total_bo).flatten()
density = gaussian_kde(flat_bo)
xs = np.linspace(flat_bo.min(), flat_bo.max(), 200)
plt.figure(figsize=(10, 6))
plt.plot(xs, density(xs), 'b-', lw=2)
plt.fill_between(xs, density(xs), alpha=0.2)
plt.xlabel('Values')
plt.ylabel('Density')
plt.title('Smooth Distribution of BO values')
plt.grid(True, alpha=0.3)
plt.show()



# # 定义区间
# bins = [(0, 0.4), (0.4, 0.8), (0.8, 1.2), (1.2, 1.6), (1.6, 2.0), (2.0, float('inf'))]
# labels = ['0-0.4', '0.4-0.8', '0.8-1.2', '1.2-1.6', '1.6-2.0', '>2']

# 计算每个区间的数据占比
# total_count = len(flat_bo)
# percentages = []

# for start, end in bins:
#     count = np.sum((flat_bo >= start) & (flat_bo < end))
#     percentage = (count / total_count) * 100
#     percentages.append(percentage)

# print(percentages)
# 绘制柱状图
# plt.figure(figsize=(10, 6))
# plt.bar(labels, percentages)
# plt.xlabel('BO Value Ranges')
# plt.ylabel('Percentage (%)')
# plt.title('Distribution of BO Values by Range')
# plt.xticks(rotation=45)
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()