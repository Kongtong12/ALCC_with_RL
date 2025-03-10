import numpy as np
from envs import env_core
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from tqdm import tqdm

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
    custom_priorities, 
    initial_parents, 
    simulation_steps=200
):
    """
    进行自定义仿真，可以指定叶节点优先级和初始父节点连接
    
    参数:
    - custom_priorities: 每个叶节点的优先级数组 (形状: agent_num)
    - initial_parents: 指定每个智能体初始连接的父节点数组 (形状: agent_num)
    - simulation_steps: 模拟步数
    
    返回:
    - results: 包含模拟结果的字典
    """
    print(f"\n开始运行自定义仿真，步数: {simulation_steps}")
    
    # 检查输入
    agent_num = len(custom_priorities)
    assert len(initial_parents) == agent_num, "优先级数组和初始父节点数组长度必须匹配"
    
    # 环境参数
    params = get_env_params(agent_num=agent_num, alpha=-1.0, beta=1.0, gamma=0.2, W1=0.4, W2=0.6)
    
    # 创建环境
    env = env_core.EnvCore(**params)
    num_agents = params['agent_num']
    parent_num = env.parent_num
    
    # 初始化指标
    total_bo = []
    action_distribution = np.zeros(11)
    total_sending_rate = 0
    total_throughput = 0
    WFI_seq = np.zeros(simulation_steps)
    throughput_seq = np.zeros(simulation_steps)
    ratio_seq = np.zeros(simulation_steps)
    sending_rates_history = []
    throughput_history = []
    priority_history = []
    
    # 重置环境
    state = env.reset()
    
    # 自定义: 覆盖默认优先级
    env.pi = custom_priorities.astype(np.float32)
    
    # 自定义: 初始父节点选择
    initial_actions = np.zeros((agent_num, parent_num))
    for i in range(agent_num):
        initial_actions[i, initial_parents[i]] = 1
    
    # 覆盖初始父节点选择
    env.current_parent = initial_actions
    env.prev_parent = initial_actions.copy()
    
    # 更新平均优先级
    env.avg_pi = env.get_avg_pi()
    
    total_reward = 0
    
    # 执行仿真步骤
    print(f"开始进行 {simulation_steps} 步的仿真...")
    for step in tqdm(range(simulation_steps), desc="仿真步骤"):
        # 第一步使用初始父节点选择
        if step == 0:
            actions = initial_actions
        else:
            # 后续步骤使用OHCA算法选择动作
            actions = env.OHCA_take_action()
        
        # 记录动作分布
        sum_one_hot = actions.sum(axis=0)
        indices = sum_one_hot.astype(int)
        action_distribution[indices] += 1
        
        # 执行动作
        next_state, reward, done, infos = env.step(actions)
        
        # 在第100步查看每个父节点包含的leaf node及其优先级
        if step == 99:  # 因为步数从0开始，所以第100步是索引99
            print("\n" + "="*60)
            print("第100步 - 每个父节点包含的叶节点及其优先级:")
            print("="*60)
            
            # 获取当前的父节点选择（current_parent是one-hot编码）
            current_parent_indices = np.argmax(env.current_parent, axis=1)
            
            # 为每个父节点创建包含的叶节点列表
            parent_to_leaves = {i: [] for i in range(parent_num)}
            
            # 收集每个父节点包含的叶节点及其优先级
            for leaf_idx in range(agent_num):
                parent_idx = current_parent_indices[leaf_idx]
                leaf_priority = env.pi[leaf_idx]
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
        
        # 提取指标
        sending_rates = np.array([info['sending_rates'] for info in infos], dtype=np.float32)
        total_sending_rate += np.sum(sending_rates)
        
        priorities = np.array([info['priority'] for info in infos], dtype=np.float32)
        throughput = np.array([info['throughput'] for info in infos], dtype=np.float32)
        total_throughput += np.sum(throughput)
        
        # 保存历史
        sending_rates_history.append(sending_rates)
        throughput_history.append(throughput)
        priority_history.append(priorities)
        
        # 计算WFI
        numerator = np.sum(throughput * priorities) ** 2
        denominator = np.sum((throughput * priorities) ** 2) * num_agents
        current_WFI = numerator / denominator if denominator > 0 else 0
        
        # 更新指标
        WFI_seq[step] = current_WFI
        throughput_seq[step] = np.sum(throughput)
        ratio_seq[step] = np.sum(throughput) / np.sum(sending_rates) if np.sum(sending_rates) > 0 else 0
        
        if step > 0:
            total_reward += np.average(reward)
            total_bo.append(next_state[0][3:6])
        
        # 更新状态
        state = next_state
    
    # 准备结果
    results = {
        'total_reward': total_reward,
        'WFI_seq': WFI_seq,
        'throughput_seq': throughput_seq,
        'ratio_seq': ratio_seq,
        'action_distribution': action_distribution / np.sum(action_distribution) if np.sum(action_distribution) > 0 else action_distribution,
        'bo_values': total_bo,
        'sending_rates_history': np.array(sending_rates_history),
        'throughput_history': np.array(throughput_history),
        'priority_history': np.array(priority_history)
    }
    
    print("\n仿真完成!")
    print(f"平均奖励: {total_reward/simulation_steps:.4f}")
    print(f"总吞吐量: {total_throughput:.4f}")
    print(f"吞吐量/发送速率比率: {total_throughput/total_sending_rate if total_sending_rate > 0 else 0:.4f}")
    
    return results

if __name__ == "__main__":
    print("\n" + "="*50)
    print("执行基于manuscript的自定义仿真 (200步)")
    print("="*50 + "\n")
    
    # 定义自定义优先级 (4个节点优先级为1，6个节点优先级为3)
    custom_priorities = np.array([1, 1, 1, 1, 3, 3, 3, 3, 3, 3])
    
    # 定义初始父节点连接 (每个值代表对应智能体初始连接的父节点，取值应为0、1或2)
    initial_parents = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2, 0])
    
    # 运行仿真
    results = custom_simulation(
        custom_priorities=custom_priorities,
        initial_parents=initial_parents,
        simulation_steps=200
    )
    
    # 保存结果
    np.save('custom_manuscript_WFI.npy', results['WFI_seq'])
    np.save('custom_manuscript_throughput.npy', results['throughput_seq'])
    np.save('custom_manuscript_ratio.npy', results['ratio_seq'])
    
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
    plt.savefig('custom_manuscript_results.png')
    plt.show() 