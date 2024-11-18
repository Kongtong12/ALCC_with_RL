import numpy as np
import env_core
env = env_core.EnvCore()
# 训练循环
num_epochs = 50
steps_per_epoch = 200
epoch_rewards = []

for epoch in range(num_epochs):
    # 重置环境
    state = env.reset()
    epoch_reward = 0
    
    # 执行时间步
    for step in range(steps_per_epoch):
        # 选择动作
        actions = env.take_action()
        
        # 执行动作并获取奖励
        next_state, reward, done, info = env.step(actions)
        
        # 累积奖励
        if step>0:
            epoch_reward += np.average(reward)
        
        # 更新状态
        state = next_state
    
    # 计算该epoch的平均奖励
    epoch_rewards.append(epoch_reward)
    
    print(f"Epoch {epoch + 1}/{num_epochs}, Average Reward: {epoch_reward:.4f}")

# 输出总体训练结果
print(f"\nTraining completed!")
print(f"Final average reward: {np.mean(epoch_rewards):.4f}")