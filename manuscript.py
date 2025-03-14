import numpy as np
from envs import env_core
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict

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

params = get_env_params(agent_num = 10, alpha=-1.0, beta=1, gamma=0.2, W1=0.4, W2=0.6)
env = env_core.EnvCore(**params)
num_agents = params['agent_num']
# 训练循环
num_epochs = 500
steps_per_epoch = 200
epoch_rewards = []
total_bo = []
total_action_dis = np.zeros(11)
total_WFI_seq = np.zeros(steps_per_epoch)
total_throughput_seq = np.zeros(steps_per_epoch)
total_ratio_seq = np.zeros(steps_per_epoch)
total_sending_rate = 0
total_throughput = 0

# 初始化数据结构来存储每个优先级的发送速率
priority_rates = defaultdict(list)  # 用于存储每个优先级的所有发送速率

for epoch in tqdm(range(num_epochs), desc="Epochs"):
    # 重置环境
    state = env.reset()
    epoch_reward = 0
    epoch_reward_1 = 0
    WFI_seq = np.zeros(steps_per_epoch)
    throughput_seq = np.zeros(steps_per_epoch)
    ratio_seq = np.zeros(steps_per_epoch)
    
    # 执行时间步
    for step in range(steps_per_epoch):
        # 选择动作
        actions = env.take_action()
        # 将actions转换为one_hot编码,对one_hot编码纵向相加，得到一个三维numpy数组，以这三个量的大小作为index加到total_action_dis中  
        sum_one_hot = actions.sum(axis=0)
        indices = sum_one_hot.astype(int)
        total_action_dis[indices] += 1
        # 执行动作并获取奖励
        next_state, reward, done, infos = env.step(actions)
        
        # 从 infos 中提取 sending_rate 和 pi
        sending_rates = np.array([info['sending_rates'] for info in infos], dtype=np.float32)  # shape: (agent_num,)
        total_sending_rate += np.sum(sending_rates)
        pis = np.array([info['priority'] for info in infos], dtype=np.float32)
        
        # 在每个时间步收集每个节点的优先级和发送速率
        for i in range(num_agents):
            priority = pis[i]
            priority_rates[priority].append(sending_rates[i])
            
        throughput = np.array([info['throughput'] for info in infos], dtype=np.float32)
        total_throughput += np.sum(throughput)
        
        # 计算分子和分母
        numerator = np.sum(throughput * pis) ** 2
        denominator = np.sum((throughput * pis) ** 2) * num_agents
        current_WFI = numerator / denominator
        WFI_seq[step] = current_WFI
        throughput_seq[step] = np.sum(throughput)
        ratio_seq[step] = np.sum(throughput) / np.sum(sending_rates)
        
        # 累积奖励
        if step:
            epoch_reward += np.average(reward)
            total_bo.append(next_state[0][3:6])
        
        # 更新状态
        state = next_state
    
    # 计算该epoch的平均奖励
    epoch_rewards.append(epoch_reward)
    total_WFI_seq += WFI_seq
    total_throughput_seq += throughput_seq
    total_ratio_seq += ratio_seq

total_WFI_seq /= num_epochs
total_throughput_seq /= num_epochs
total_ratio_seq /= num_epochs

# 保存数据
np.save('NGECC_WFI.npy', total_WFI_seq)
np.save('NGECC_throughput.npy', total_throughput_seq)
np.save('NGECC_ratio.npy', total_ratio_seq)

# 输出总体训练结果
print(f"Total throughput: {total_throughput:.4f}")
print(f"deliver ratio: {total_throughput/total_sending_rate:.4f}")
print(f"Final average reward: {np.mean(epoch_rewards):.4f}")

# 计算并显示每个优先级的统计信息
print("\nPriority Level Statistics:")
print("-" * 50)
print("Priority | Avg Sending Rate | Sample Count | Min Rate | Max Rate")
print("-" * 50)

for priority in sorted(priority_rates.keys()):
    rates = np.array(priority_rates[priority])
    avg_rate = np.mean(rates)
    count = len(rates)
    min_rate = np.min(rates)
    max_rate = np.max(rates)
    print(f"{priority:8.2f} | {avg_rate:14.4f} | {count:12d} | {min_rate:8.4f} | {max_rate:8.4f}")

# 绘制优先级与发送速率的关系图
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
priorities = sorted(priority_rates.keys())
avg_rates = [np.mean(priority_rates[p]) for p in priorities]
plt.bar([f"{p:.2f}" for p in priorities], avg_rates)
plt.title('Average Sending Rates by Priority Level')
plt.xlabel('Priority')
plt.ylabel('Average Sending Rate')
plt.xticks(rotation=45)

# 添加箱型图显示发送速率的分布
plt.subplot(1, 2, 2)
box_data = [priority_rates[p] for p in priorities]
plt.boxplot(box_data, labels=[f"{p:.2f}" for p in priorities])
plt.title('Sending Rate Distribution by Priority')
plt.xlabel('Priority')
plt.ylabel('Sending Rate')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 绘制WFI序列
plt.figure(figsize=(10, 6))
plt.plot(total_WFI_seq)
plt.title('WFI Sequence')
plt.xlabel('Index')
plt.ylabel('WFI Value')
plt.show()

# print("total_action_dis:", total_action_dis / total_action_dis.sum())
# # 绘制total_action_dis / total_action_dis.sum()的柱状图
# plt.figure(figsize=(10, 6))
# plt.bar(range(11), total_action_dis / total_action_dis.sum())
# plt.xlabel('Actions')
# plt.ylabel('Percentage (%)')
# plt.title('Distribution of Actions')
# plt.xticks(range(11))
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

# # 使用KDE绘制平滑的密度分布曲线
# flat_bo = np.array(total_bo).flatten()
# density = gaussian_kde(flat_bo)
# xs = np.linspace(flat_bo.min(), flat_bo.max(), 200)
# plt.figure(figsize=(10, 6))
# plt.plot(xs, density(xs), 'b-', lw=2)
# plt.fill_between(xs, density(xs), alpha=0.2)
# plt.xlabel('Values')
# plt.ylabel('Density')
# plt.title('Smooth Distribution of BO values')
# plt.grid(True, alpha=0.3)
# plt.show()
# # 定义区间
# bins = [(0, 0.4), (0.4, 0.8), (0.8, 1.2), (1.2, 1.6), (1.6, 2.0), (2.0, float('inf'))]
# labels = ['0-0.4', '0.4-0.8', '0.8-1.2', '1.2-1.6', '1.6-2.0', '>2']

# # 计算每个区间的数据占比
# total_count = len(flat_bo)
# percentages = []

# for start, end in bins:
#     count = np.sum((flat_bo >= start) & (flat_bo < end))
#     percentage = (count / total_count) * 100
#     percentages.append(percentage)

# print(percentages)
# # 绘制柱状图
# plt.figure(figsize=(10, 6))
# plt.bar(labels, percentages)
# plt.xlabel('BO Value Ranges')
# plt.ylabel('Percentage (%)')
# plt.title('Distribution of BO Values by Range')
# plt.xticks(rotation=45)
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()