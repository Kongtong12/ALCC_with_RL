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

params = get_env_params(agent_num = 10, alpha=-1.0, beta=1, gamma=0.2, W1=0.4, W2=0.6)
env = env_core.EnvCore(**params)
# 训练循环
num_epochs = 500
steps_per_epoch = 200
epoch_rewards = []
epoch_rewards_1 = []
epoch_rewards_2 = []
epoch_rewards_3 = []
total_bo = []
total_action_dis = np.zeros(11)

for epoch in tqdm(range(num_epochs), desc="Epochs"):
    # 重置环境
    state = env.reset()
    epoch_reward = 0
    epoch_reward_1 = 0
    epoch_reward_2 = 0
    epoch_reward_3 = 0
    
    # 执行时间步
    for step in range(steps_per_epoch):
        # 选择动作
        actions = env.take_action()
        # 将actions转换为one_hot编码,对one_hot编码纵向相加，得到一个三维numpy数组，以这三个量的大小作为index加到total_action_dis中  
        sum_one_hot = actions.sum(axis=0)
        indices = sum_one_hot.astype(int)
        total_action_dis[indices] += 1
        # 执行动作并获取奖励
        next_state, reward, done, info = env.step(actions)
        reward_1, reward_2, reward_3 = env.get_reward()
        
        # 累积奖励
        if step:
            epoch_reward += np.average(reward)
            epoch_reward_1 += np.average(reward_1)
            epoch_reward_2 += np.average(reward_2)
            epoch_reward_3 += np.average(reward_3)
            total_bo.append(next_state[0][3:6])
        
        # 更新状态
        state = next_state
    
    # 计算该epoch的平均奖励
    epoch_rewards.append(epoch_reward)
    epoch_rewards_1.append(epoch_reward_1)
    epoch_rewards_2.append(epoch_reward_2)
    epoch_rewards_3.append(epoch_reward_3)
    
    #print(f"Epoch {epoch + 1}/{num_epochs}, Average Reward: {epoch_reward:.4f}")

# 输出总体训练结果
#print(f"\nTraining completed!")
print(f"Final average reward: {np.mean(epoch_rewards):.4f}")
print(f"Final average reward_1: {np.mean(epoch_rewards_1):.4f}")
print(f"Final average reward_2: {np.mean(epoch_rewards_2):.4f}")
print(f"Final average reward_3: {np.mean(epoch_rewards_3):.4f}")

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