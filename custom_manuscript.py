import numpy as np
from envs import env_core
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
    # print(f"\n开始运行自定义仿真，步数: {simulation_steps}")
    
    # 检查输入
    agent_num = len(custom_priorities)
    assert len(initial_parents) == agent_num, "优先级数组和初始父节点数组长度必须匹配"
    
    # 环境参数
    params = get_env_params(agent_num=agent_num, alpha=-1.0, beta=1.0, gamma=0.2, W1=0.4, W2=0.6)
    
    # 创建环境
    env = env_core.EnvCore(**params)
    num_agents = params['agent_num']
    parent_num = env.parent_num
    
    # 初始化每个节点的发送速率历史记录
    node_sending_rates = [[] for _ in range(num_agents)]
    node_throughput = [[] for _ in range(num_agents)]
    
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
    # print(f"开始进行 {simulation_steps} 步的仿真...")
    for step in range(simulation_steps):
        # 第一步使用初始父节点选择
        if step == 0:
            actions = initial_actions
        else:
            # 后续步骤使用take_action算法选择动作
            actions = env.OHCA_take_action()
        
        # 记录动作分布
        sum_one_hot = actions.sum(axis=0)
        indices = sum_one_hot.astype(int)
        action_distribution[indices] += 1
        
        # 执行动作
        next_state, reward, done, infos = env.step(actions)
        
        # 记录每个节点的发送速率和吞吐量
        sending_rates = np.array([info['sending_rates'] for info in infos], dtype=np.float32)
        throughput = np.array([info['throughput'] for info in infos], dtype=np.float32)
        
        for i in range(num_agents):
            node_sending_rates[i].append(sending_rates[i])
            node_throughput[i].append(throughput[i])
        
        # 提取指标
        total_sending_rate += np.sum(sending_rates)
        total_throughput += np.sum(throughput)
        
        # 保存历史
        sending_rates_history.append(sending_rates)
        throughput_history.append(throughput)
        priority_history.append(custom_priorities)
        
        # 计算WFI
        numerator = np.sum(throughput * custom_priorities) ** 2
        denominator = np.sum((throughput * custom_priorities) ** 2) * num_agents
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
    
    # 计算并显示每个节点的统计信息
    # print("\n每个节点的统计信息:")
    # print("="*80)
    # print("节点ID | 优先级 | 平均发送速率 | 平均吞吐量 | 发送速率标准差 | 吞吐量标准差 | 传输效率")
    # print("="*80)
    
    node_stats = []
    for i in range(num_agents):
        avg_sending_rate = np.mean(node_sending_rates[i])
        avg_throughput = np.mean(node_throughput[i])
        std_sending_rate = np.std(node_sending_rates[i])
        std_throughput = np.std(node_throughput[i])
        efficiency = avg_throughput / avg_sending_rate if avg_sending_rate > 0 else 0
        
        stats = {
            'node_id': i,
            'priority': custom_priorities[i],
            'avg_sending_rate': avg_sending_rate,
            'avg_throughput': avg_throughput,
            'std_sending_rate': std_sending_rate,
            'std_throughput': std_throughput,
            'efficiency': efficiency
        }
        node_stats.append(stats)
        
        # print(f"{i:6d} | {custom_priorities[i]:7.2f} | {avg_sending_rate:12.4f} | "
        #       f"{avg_throughput:11.4f} | {std_sending_rate:14.4f} | "
        #       f"{std_throughput:13.4f} | {efficiency:8.4f}")
    

    
    # 原有的结果返回
    results = {
        'total_reward': total_reward,
        'WFI_seq': WFI_seq,
        'throughput_seq': throughput_seq,
        'ratio_seq': ratio_seq,
        'action_distribution': action_distribution / np.sum(action_distribution) if np.sum(action_distribution) > 0 else action_distribution,
        'bo_values': total_bo,
        'sending_rates_history': np.array(sending_rates_history),
        'throughput_history': np.array(throughput_history),
        'priority_history': np.array(priority_history),
        'node_stats': node_stats  # 添加节点统计信息到结果中
    }
    
    # print("\n仿真完成!")
    # print(f"平均奖励: {total_reward/simulation_steps:.4f}")
    # print(f"总吞吐量: {total_throughput:.4f}")
    # print(f"吞吐量/发送速率比率: {total_throughput/total_sending_rate if total_sending_rate > 0 else 0:.4f}")
    
    return results

if __name__ == "__main__":
    print("\n" + "="*50)
    print("执行基于manuscript的自定义仿真 (500个epoch，每epoch 200步)")
    print("="*50 + "\n")
    
    # 定义仿真参数
    simulation_steps = 200
    num_epochs = 500
    agent_num = 10
    
    # 定义初始父节点连接 (每个值代表对应智能体初始连接的父节点，取值应为0、1或2)
    initial_parents = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2, 0])
    
    # 初始化结果累加器
    total_WFI_seq = np.zeros(simulation_steps)
    total_throughput_seq = np.zeros(simulation_steps)
    total_ratio_seq = np.zeros(simulation_steps)
    total_reward = 0
    
    # 运行500个epoch的仿真
    for epoch in tqdm(range(num_epochs), desc="Epochs"):
        # 每个epoch随机生成1-3之间的优先级向量
        random_priorities = np.random.randint(1, 4, size=agent_num).astype(np.float32)
        
        # 运行单次仿真
        results = custom_simulation(
            custom_priorities=random_priorities,
            initial_parents=initial_parents,
            simulation_steps=simulation_steps
        )
        
        # 累加结果
        total_WFI_seq += results['WFI_seq']
        total_throughput_seq += results['throughput_seq']
        total_ratio_seq += results['ratio_seq']
        total_reward += results['total_reward']
    
    # 计算平均结果
    avg_WFI_seq = total_WFI_seq / num_epochs
    avg_throughput_seq = total_throughput_seq / num_epochs
    avg_ratio_seq = total_ratio_seq / num_epochs
    avg_reward = total_reward / num_epochs
    
    # 保存结果
    np.save('OHCA_WFI.npy', avg_WFI_seq)
    np.save('OHCA_throughput.npy', avg_throughput_seq)
    np.save('OHCA_ratio.npy', avg_ratio_seq)
    
    # 输出总体训练结果
    print("\n" + "="*50)
    print(f"500个epoch平均结果:")
    print(f"平均奖励: {avg_reward/simulation_steps:.4f}")
    print(f"平均WFI: {np.mean(avg_WFI_seq):.4f}")
    print(f"平均吞吐量: {np.mean(avg_throughput_seq):.4f}")
    print(f"平均吞吐率: {np.mean(avg_ratio_seq):.4f}")
    print("="*50 + "\n")
    
    # 可视化结果
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(avg_WFI_seq)
    plt.title('Average Weighted Fairness Index (WFI)')
    plt.xlabel('Steps')
    plt.ylabel('WFI')
    
    plt.subplot(2, 2, 2)
    plt.plot(avg_throughput_seq)
    plt.title('Average Total Throughput')
    plt.xlabel('Steps')
    plt.ylabel('Throughput')
    
    plt.subplot(2, 2, 3)
    plt.plot(avg_ratio_seq)
    plt.title('Average Throughput/Sending Rate Ratio')
    plt.xlabel('Steps')
    plt.ylabel('Ratio')
    
    plt.tight_layout()
    plt.savefig('OHCA_avg_results.png')
    plt.show() 