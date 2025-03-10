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
from tqdm import tqdm

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

def custom_simulation(
    actor_path, 
    custom_priorities, 
    initial_parents, 
    simulation_steps=200
):
    """
    Run a custom simulation with specified leaf node priorities and initial parent connections.
    
    Parameters:
    - actor_path: Path to the trained actor model
    - custom_priorities: Array of priorities for each leaf node (shape: agent_num)
    - initial_parents: Array specifying initial parent node for each agent (shape: agent_num)
    - simulation_steps: Number of simulation steps to run
    
    Returns:
    - results: Dictionary containing simulation results
    """
    print(f"\n正在运行单次模拟，步数: {simulation_steps}")
    
    # Check inputs
    agent_num = len(custom_priorities)
    assert len(initial_parents) == agent_num, "Number of priorities and initial parents must match"
    
    # Load the model
    checkpoint = torch.load(actor_path, map_location=torch.device('cuda'))
    if isinstance(checkpoint, dict):
        if 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
    
    # Parse arguments
    parser = get_config()
    all_args = parse_args(sys.argv[1:], parser)
    
    # 下面修改默认的参数
    all_args.share_policy = True
    all_args.num_agents = agent_num
    all_args.num_env_steps = 3 * 1e5
    all_args.use_eval = True
    # 下面是一些参数的定义
    episode_length = simulation_steps  # 使用传入的步数而不是默认值
    n_rollout_threads = 1
    num_agents = agent_num
    recurrent_N = all_args.recurrent_N
    hidden_size = all_args.hidden_size
    parent_num = 3
    
    # Environment parameters
    params = get_env_params(agent_num=agent_num, alpha=-1.0, beta=1.0, gamma=0.2, W1=0.4, W2=0.6)
    
    # Create environment
    env = DiscreteActionEnv(**params)
    
    # Create actor model
    actor = R_Actor(all_args, env.observation_space[0], env.action_space[0], device=torch.device('cuda'))
    actor.load_state_dict(state_dict)
    
    # Initialize RNN states and masks
    rnn_states = np.zeros((episode_length + 1, n_rollout_threads, num_agents, recurrent_N, hidden_size), dtype=np.float32).shape[2:]
    eval_rnn_states = np.zeros((1, *rnn_states), dtype=np.float32)
    eval_masks = np.ones((n_rollout_threads, num_agents, 1), dtype=np.float32)
    
    # Initialize metrics
    action_distribution = np.zeros(11)  # 根据原始代码的大小
    total_throughput = 0
    total_sending_rate = 0
    total_rewards = 0
    WFI_seq = np.zeros(episode_length)
    throughput_seq = np.zeros(episode_length)
    ratio_seq = np.zeros(episode_length)
    bo_values = []
    sending_rates_history = []
    throughput_history = []
    priority_history = []
    
    # Reset the environment
    obs = env.reset()
    
    # 自定义: 覆盖默认优先级
    env.env.pi = custom_priorities.astype(np.float32)
    
    # 自定义: 转换initial_parents为one-hot编码
    initial_actions_env = np.zeros((num_agents, parent_num))
    for i in range(num_agents):
        initial_actions_env[i, initial_parents[i]] = 1
    
    # 自定义: 覆盖初始父节点选择
    env.env.current_parent = initial_actions_env
    env.env.prev_parent = initial_actions_env.copy()
    
    # 自定义: 更新基于初始连接的平均优先级
    env.env.avg_pi = env.env.get_avg_pi()
    
    # 运行模拟
    print(f"开始进行 {episode_length} 步的模拟...")
    for step in tqdm(range(episode_length), desc=f"模拟步骤"):
        # 对于第一步，使用初始父节点
        if step == 0:
            actions_env = initial_actions_env
            # 直接调用step，不使用神经网络
            obs, rewards, dones, infos = env.step(actions_env)
        else:
            # 对后续步骤使用神经网络
            actions, _, rnn_states = actor(obs, eval_rnn_states, eval_masks, deterministic=False)
            actions = _t2n(actions)
            
            # 将actions转换为one-hot编码
            one_hot = np.eye(env.action_space[0].n)[actions]
            sum_one_hot = one_hot.sum(axis=0)
            indices = sum_one_hot.astype(int)
            action_distribution[indices] += 1
            
            actions_env = np.squeeze(np.eye(env.action_space[0].n)[actions], 1)
            obs, rewards, dones, infos = env.step(actions_env)
        
        # 在第100步查看每个父节点包含的leaf node及其优先级
        if step == 99:  # 因为步数从0开始，所以第100步是索引99
            print("\n" + "="*60)
            print("第100步 - 每个父节点包含的叶节点及其优先级:")
            print("="*60)
            
            # 获取当前的父节点选择（current_parent是one-hot编码）
            current_parent_indices = np.argmax(env.env.current_parent, axis=1)
            
            # 为每个父节点创建包含的叶节点列表
            parent_to_leaves = {i: [] for i in range(parent_num)}
            
            # 收集每个父节点包含的叶节点及其优先级
            for leaf_idx in range(agent_num):
                parent_idx = current_parent_indices[leaf_idx]
                leaf_priority = env.env.pi[leaf_idx]
                parent_to_leaves[parent_idx].append((leaf_idx, leaf_priority))
            
            # 打印每个父节点的信息
            for parent_idx, leaves in parent_to_leaves.items():
                print(f"\n父节点 {parent_idx}:")
                if not leaves:
                    print("  没有连接的叶节点")
                else:
                    total_priority = sum(priority for _, priority in leaves)
                    print(f"  连接的叶节点数量: {len(leaves)}")
                    print(f"  总优先级: {total_priority:.2f}")
                    print(f"  平均优先级: {total_priority/len(leaves) if leaves else 0:.2f}")
                    print("  叶节点列表 (节点ID, 优先级):")
                    for leaf_idx, priority in leaves:
                        print(f"    叶节点 {leaf_idx}: 优先级 {priority:.2f}")
            
            print("\n" + "="*60)
        
        # 从 infos 中提取指标
        sending_rates = np.array([info['sending_rates'] for info in infos], dtype=np.float32)
        priorities = np.array([info['priority'] for info in infos], dtype=np.float32)
        throughput = np.array([info['throughput'] for info in infos], dtype=np.float32)
        
        # 保存历史
        sending_rates_history.append(sending_rates)
        throughput_history.append(throughput)
        priority_history.append(priorities)
        
        # 更新总计
        total_sending_rate += np.sum(sending_rates)
        total_throughput += np.sum(throughput)
        
        # 计算加权公平指数 (WFI)
        numerator = np.sum(throughput * priorities) ** 2
        denominator = np.sum((throughput * priorities) ** 2) * num_agents
        current_WFI = numerator / denominator if denominator > 0 else 0
        
        # 更新指标
        WFI_seq[step] = current_WFI
        throughput_seq[step] = np.sum(throughput)
        ratio_seq[step] = np.sum(throughput) / np.sum(sending_rates) if np.sum(sending_rates) > 0 else 0
        
        if step > 0:
            bo_values.append(obs[0][parent_num:2*parent_num])
        
        total_rewards += np.average(rewards)
    
    # 准备结果
    results = {
        'total_rewards': total_rewards,
        'WFI_seq': WFI_seq,
        'throughput_seq': throughput_seq,
        'ratio_seq': ratio_seq,
        'action_distribution': action_distribution / max(1, np.sum(action_distribution)),
        'bo_values': bo_values,
        'sending_rates_history': np.array(sending_rates_history),
        'throughput_history': np.array(throughput_history),
        'priority_history': np.array(priority_history),
        'total_throughput': total_throughput,
        'total_sending_rate': total_sending_rate
    }
    
    print("\n模拟完成!")
    print(f"平均奖励: {total_rewards/episode_length:.4f}")
    print(f"总吞吐量: {total_throughput:.4f}")
    print(f"吞吐量/发送速率比率: {total_throughput/total_sending_rate if total_sending_rate > 0 else 0:.4f}")
    
    return results

# 获取当前文件的父目录
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "."))

# 将父目录添加到sys.path
sys.path.append(parent_dir)

from config import get_config

if __name__ == "__main__":
    print("\n" + "="*50)
    print("执行自定义模拟 (200步)")
    print("="*50 + "\n")
    
    # 加载的actor模型路径
    actor_path = r'results\MyEnv\MyEnv\mappo\check\run59\models\actor.pt'
    
    # 定义自定义优先级 (4个节点优先级为1，6个节点优先级为3)
    custom_priorities = np.array([1, 1, 1, 1, 3, 3, 3, 3, 3, 3])
    
    # 定义初始父节点连接 (每个值代表对应智能体初始连接的父节点，取值应为0、1或2)
    initial_parents = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2, 0])
    
    # 运行模拟
    results = custom_simulation(
        actor_path=actor_path,
        custom_priorities=custom_priorities,
        initial_parents=initial_parents,
        simulation_steps=200
    )
    
    # 保存结果
    np.save('custom_WFI.npy', results['WFI_seq'])
    np.save('custom_throughput.npy', results['throughput_seq'])
    np.save('custom_ratio.npy', results['ratio_seq'])
    
    # 可视化结果
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(results['WFI_seq'])
    plt.title('Weighted Fairness Index (WFI)')
    plt.xlabel('Steps')
    plt.ylabel('WFI')
    
    plt.subplot(2, 2, 2)
    plt.plot(results['throughput_seq'])
    plt.title('Total Throughput')
    plt.xlabel('Steps')
    plt.ylabel('Throughput')
    
    plt.subplot(2, 2, 3)
    plt.plot(results['ratio_seq'])
    plt.title('Throughput/Sending Rate Ratio')
    plt.xlabel('Steps')
    plt.ylabel('Ratio')
    
    plt.subplot(2, 2, 4)
    parent_labels = ['Parent 0', 'Parent 1', 'Parent 2']
    plt.bar(parent_labels, results['action_distribution'][:3])
    plt.title('Action Distribution')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('custom_simulation_results.png')
    plt.show()