import numpy as np

#问题：如果这里numpy整数和小数做乘除会怎样，比如self.pi = np.ones(self.agent_num)
class EnvCore(object):
    """
    # 环境中的智能体
    """

    def __init__(self, **kwargs):
        self.if_rand_pi = True # 是否随机初始化优先级
        self.agent_num = kwargs.get('agent_num', 10)  # 设置智能体的个数，leaf node的数量为10
        self.parent_num = 3  # 父节点数量
        if self.if_rand_pi:
            self.obs_dim = 2 * self.parent_num + 2  # 每个parent node对应的ETX，bo,自身的优先级,上一个时刻的parent node选择
        else:
            self.obs_dim = 2 * self.parent_num + 1
        self.action_dim = self.parent_num  # 设置智能体的动作维度，这里对应parent node的个数


        self.pi = np.ones(self.agent_num) # 每个节点的优先级，用于计算收益。在这里简化为所有节点拥有相同的优先级
        #下面定义的是选择父亲节点后，leaf node的payoff function
        self.w1 = 15.
        self.w2 = 3.
        self.w3 = 0.9
        self.xi_max = np.full(self.agent_num,8.0) # 这里设置了每个节点的最大传输速率

        # 初始化奖励参数，使用kwargs传递
        self.alpha = kwargs.get('alpha', -1.0)
        self.beta = kwargs.get('beta', 1.0)
        self.gamma = kwargs.get('gamma', 1.0)
        self.W1 = kwargs.get('W1', 0.4)
        self.W2 = kwargs.get('W2', 0.6)
        

    def reset(self):
        """
        # self.agent_num设定为2个智能体时，返回值为一个list，每个list里面为一个shape = (self.obs_dim, )的观测数据
        # When self.agent_num is set to 2 agents, the return value is a list, each list contains a shape = (self.obs_dim, ) observation data
        """
        # 初始化 ETX 值（叶节点到父节点的链路质量）
        self.etx = np.random.uniform(1.0, 5.0, size=(self.agent_num, self.parent_num))
        # 初始化 BO 值（上一个时刻进入父节点的流量），初始化为 0
        self.bo = np.zeros(self.parent_num)
        #初始化每个父亲节点的最大传输速率
        self.xi_out = np.array([15.,15.,15.])

        # 初始化智能体的上一个父节点选择，随机分配或设为 -1（表示初始状态）
        self.prev_parent = np.zeros([self.agent_num, self.parent_num])  # -1 表示未选择任何父节点

        #开始时刻，初始化所有leaf node的发送速率为0
        self.sending_rates = np.zeros(self.agent_num)  # 所有智能体的发送速率

        # 初始化每个智能体的优先级，在1到3之间连续选择，形状为 (parent_num,)
        if self.if_rand_pi:
            self.pi = np.random.randint(1, 4, size=self.agent_num)

        # 返回初始观测
        return self._get_obs()

    def step(self, actions):
        """
        执行一步环境更新

        参数:
        - actions: 一个长度为 agent_num 的数组，每个元素是智能体选择的父节点索引（0、1、2）

        返回:
        - obs_n: 智能体的新观测
        - reward_n: 智能体的奖励
        - done_n: 智能体的完成标志（此处全为 False）
        - info_n: 额外信息（此处为空字典）
        """
        # 更新智能体的父节点选择
        self.current_parent = actions

        # 计算切换惩罚
        #这里有一个很重大的改变！！！！
        switch_penalty = 1 - np.all(self.current_parent == self.prev_parent, axis=1).astype(np.float32)
        self.prev_parent = self.current_parent.copy()

        # 更新 ETX（可加入动态变化，此处简单模拟随机波动）注意，在这里需要设置偏好
        etx_fluctuation = np.random.normal(0, 0.1, size=(self.agent_num, self.parent_num))
        self.etx += etx_fluctuation
        self.etx = np.clip(self.etx, 1.0, 5.0)

        # 更新上一个时间节点进入父节点的Bo,发送速率,奖励
        self._update_bo()
        self._compute_sending_rates()
        # 下面做一下简单尝试 
        rewards = self._compute_rewards(switch_penalty)
        '''rewards1 = []
        for i in range(self.agent_num):
            rewards1.append([np.random.rand()])'''
        # 获取新的观测
        obs = self._get_obs()
        dones = [False] * self.agent_num
        infos = [{} for _ in range(self.agent_num)]
        return [obs, rewards, dones, infos]

        '''        sub_agent_obs = []
        sub_agent_reward = []
        sub_agent_done = []
        sub_agent_info = []
        for i in range(self.agent_num):
            sub_agent_obs.append(np.random.random(size=(14,)))
            sub_agent_reward.append([np.random.rand()])
            sub_agent_done.append(False)
            sub_agent_info.append({})

        return [sub_agent_obs, sub_agent_reward, sub_agent_done, sub_agent_info]'''
    
    def _get_obs(self):
        """
        获取智能体的观测

        返回:
        - obs_n: 一个长度为 agent_num 的列表，每个元素是对应智能体的观测向量
        """
        obs_n = []
        for i in range(self.agent_num):
            # 获取智能体与所有父节点的 ETX 值
            etx_obs = self.etx[i]  # 形状为 (parent_num,)

            # 获取所有父节点的 BO 值
            bo_obs = self.bo  # 形状为 (parent_num,)

            # 获取智能体的优先级
            pi_obs = self.pi[i]

            # 获取智能体的上一个父节点选择
            prev_parent_obs = np.array([self.prev_parent[i]])  # 形状为 (1,)

            # 拼接观测向量
            if self.if_rand_pi:
                obs = np.concatenate([etx_obs, bo_obs, np.array([pi_obs]), np.argmax(prev_parent_obs, axis=1)])
            else:
                obs = np.concatenate([etx_obs, bo_obs, np.argmax(prev_parent_obs, axis=1)])

            obs_n.append(obs)

        return obs_n

    def _compute_sending_rates(self):
        """
        计算智能体的最优发送速率
        """
        current_parent = np.argmax(self.current_parent, axis=1)
        counts = np.bincount(current_parent, minlength=self.parent_num)
        # 下面为计算的过程
        counts_w2 = counts * self.w2 / (self.xi_out + 1)
        for i in range(self.agent_num):
            parent_idx = current_parent[i]
            if (counts_w2[parent_idx] + self.w3 * self.pi[i] >= self.w1):
                self.sending_rates[i] = 0
            elif (counts_w2[parent_idx] + self.w3 * self.pi[i] <= self.w1 / (1 + self.xi_max[i])):
                self.sending_rates[i] = self.xi_max[i]
            else:
                self.sending_rates[i] = -1+self.w1*(1+self.xi_out[parent_idx])/(self.w2*counts[parent_idx]+self.w3*self.pi[i]*(self.xi_out[parent_idx]+1))


    def _update_bo(self):
        """
        更新时间节点进入父亲节点的流量
        """
        # 重置 BO
        self.bo = np.zeros(self.parent_num)
        current_parent = np.argmax(self.current_parent, axis=1)
        # 累加每个父节点接收到的发送速率
        for j in range(self.parent_num):
            # 获取选择了父节点 j 的智能体索引
            agents_selecting_j = np.where(current_parent == j)[0]

            # 累加这些智能体的发送速率
            total_rate = np.sum(self.sending_rates[agents_selecting_j])
            # 修改了bo的计算方式

            self.bo[j] = total_rate / self.xi_out[j]

    def _compute_rewards(self, switch_penalty):
        """
        计算智能体的奖励

        参数:
        - switch_penalty: 一个长度为 agent_num 的数组，表示每个智能体是否切换了父节点

        返回:
        - rewards: 一个长度为 agent_num 的列表，表示每个智能体的奖励
        """
        rewards = []
        #定义了三个奖励
        self.rewards_1 = []
        self.rewards_2 = []
        self.rewards_3 = []

        current_parent = np.argmax(self.current_parent, axis=1)
        for i in range(self.agent_num):
            parent_idx = current_parent[i]

            #这里我希望对self.bo进行更新，使得若某一个位置大于1，则将其设置为1
            bo = np.minimum(self.bo,1)
            # 计算 OF1
            of1 = self.W1 * self.etx[i, parent_idx] + self.W2 * bo[parent_idx]

            # 计算 Omega_i（此处简化处理）
            omega_i = self._compute_omega_i(i, parent_idx)

            reward_1 = self.alpha * of1
            reward_2 = self.beta * omega_i
            reward_3 = self.gamma * switch_penalty[i]

            # 计算奖励
            reward = self.alpha * of1 + self.beta * omega_i - self.gamma * switch_penalty[i]

            self.rewards_1.append([reward_1])
            self.rewards_2.append([reward_2])
            self.rewards_3.append([reward_3])
            rewards.append([reward])

        return rewards
    

    def _compute_omega_i(self, agent_idx, parent_idx):
        """
        计算智能体的 Omega_i 值

        参数:
        - agent_idx: 智能体索引
        - parent_idx: 父节点索引

        返回:
        - omega_i: 智能体的发送速率部分的收益
        """

        current_parent = np.argmax(self.current_parent, axis=1)
        # 获取连接到该父节点的智能体数量 n
        n = np.sum(current_parent == parent_idx)

        xi_out = self.xi_out[parent_idx] # 特定parent node的传输速率

        # 计算 Omega_i
        numerator = np.sum(self.sending_rates[current_parent == parent_idx]) + 1
        denominator = xi_out + 1

        omega_i = self.w1 * np.log(self.sending_rates[agent_idx] + 1) \
                  - self.w2 * n * (numerator / denominator) \
                  - self.w3 * self.pi[agent_idx] * self.sending_rates[agent_idx]
        return omega_i
    
    def take_action(self):
        """
        选择动作，使用矩阵运算优化性能

        返回:
        - actions: 智能体选择的父节点的one-hot编码矩阵 (agent_num, parent_num)
        """
        # 计算所有智能体的OF1值矩阵 (agent_num, parent_num)
        of1_values = 0.4 * self.etx + 0.6 * self.bo[np.newaxis, :]
        
        # 为所有智能体创建切换惩罚矩阵
        prev_parents = np.argmax(self.prev_parent, axis=1)
        switch_penalty = np.ones((self.agent_num, self.parent_num))
        switch_penalty -= self.prev_parent
        
        # 添加切换惩罚
        of1_values += 0.8*switch_penalty
        
        # 找到每个智能体的最优父节点
        best_parents = np.argmin(of1_values, axis=1)
        
        # 创建one-hot编码矩阵
        actions = np.zeros((self.agent_num, self.parent_num))
        actions[np.arange(self.agent_num), best_parents] = 1
        
        return actions
    
    def get_reward(self):
        return self.rewards_1, self.rewards_2, self.rewards_3
