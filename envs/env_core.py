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
        self.obs_dim = 4 * self.parent_num + 1  # 每个parent node对应的bo，xi_in, pi的综合状态 ,自身的优先级,上一个时刻的parent node选择
        self.action_dim = self.parent_num  # 设置智能体的动作维度，这里对应parent node的个数


        self.pi = np.ones(self.agent_num) # 每个节点的优先级，用于计算收益。在这里简化为所有节点拥有相同的优先级
        #下面定义的是选择父亲节点后，leaf node的payoff function
        self.w1 = 15.
        self.w2 = 9.
        self.w5 = 12.8
        self.w3 = .9 * self.w5
        self.w4 = 1. * self.w5
        self.xi_max = np.full(self.agent_num,6.) # 这里设置了每个节点的最大传输速率

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
        self.etx = np.random.uniform(1.00, 1.02, size=(self.agent_num, self.parent_num))
        # 初始化 BO 值（上一个时刻进入父节点的流量），初始化为 0
        self.bo = np.zeros(self.parent_num)
        #初始化每个父亲节点的最大传输速率
        
        self.xi_out_base = np.array([12.8,12.8,12.8])
        # 这里的xi_out用来存储预测值
        self.xi_out = self.xi_out_base
        self.xi_out_2 = self.xi_out_base
        self.xi_out_1 = self.xi_out_base

        # 初始化智能体的上一个父节点选择，随机分配或设为 -1（表示初始状态）
        self.prev_parent = np.zeros([self.agent_num, self.parent_num])  # -1 表示未选择任何父节点
        self.current_parent = np.zeros([self.agent_num, self.parent_num])  # -1 表示未选择任何父节点

        #开始时刻，初始化所有leaf node的发送速率为0
        self.sending_rates = np.zeros(self.agent_num)  # 所有智能体的发送速率

        # 初始化每个智能体的优先级，在1到3之间连续选择，形状为 (parent_num,)
        self.pi = np.random.randint(1, 4, size=self.agent_num)
        self.pi = self.pi.astype(np.float32)

        self.avg_pi = np.zeros(self.parent_num)

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
        # TODO check if the bo is suitable
        # self._update_bo()
        self.current_parent = actions

        # 计算切换惩罚
        #这里有一个很重大的改变！！！！
        switch_penalty = 1 - np.all(self.current_parent == self.prev_parent, axis=1).astype(np.float32)
        self.prev_parent = self.current_parent.copy()

        # 更新 ETX（可加入动态变化，此处简单模拟随机波动）注意，在这里需要设置偏好
        etx_fluctuation = np.random.normal(0, 0.01, size=(self.agent_num, self.parent_num))
        self.etx += etx_fluctuation
        self.etx = np.clip(self.etx, 1.00, 1.02)

        # 更新选择新的拓扑下的avg_pi
        self.avg_pi = self.get_avg_pi()

        # 计算智能体的发送速率
        self._compute_sending_rates()

        # 更新每个节点的xi_out
        new_xi_out = np.clip(0.7 * self.xi_out_1 + 0.3 * self.xi_out_base + np.random.normal(0, 1, size=(self.parent_num,)), 10, 15)
        self.xi_out_2 = self.xi_out_1
        self.xi_out_1 = new_xi_out



        # 更新上一个时间节点进入父节点的Bo,发送速率,奖励
        

        # 下面做一下简单尝试 
        rewards = self._compute_rewards(switch_penalty)

        # TODO bo
        # bo = np.zeros(self.parent_num)
        current_parent = np.argmax(self.current_parent, axis=1)
        # 累加每个父节点接收到的发送速率
        for j in range(self.parent_num):
            # 获取选择了父节点 j 的智能体索引
            agents_selecting_j = np.where(current_parent == j)[0]
            # 累加这些智能体的发送速率
            total_rate = np.sum(self.sending_rates[agents_selecting_j] / self.etx[agents_selecting_j, j])
            # 修改了bo的计算方式
            self.bo[j] = total_rate / new_xi_out[j]

        # 获取新的观测
        obs = self._get_obs()
        dones = [False] * self.agent_num
        infos = [{} for _ in range(self.agent_num)]

        # 填充 infos 中的发送速率和优先级
        for i in range(self.agent_num):
            infos[i]['sending_rates'] = self.sending_rates[i]
            infos[i]['priority'] = self.pi[i]
            infos[i]['throughput'] = self.sending_rates[i] / (self.etx[i, np.argmax(self.current_parent[i])] * np.maximum(self.bo[np.argmax(self.current_parent[i])], 1))
        
        return [obs, rewards, dones, infos]
    
    def _get_obs(self):
        """
        获取智能体的观测

        返回:
        - obs_n: 一个长度为 agent_num 的列表，每个元素是对应智能体的观测向量
        """
        obs_n = []
        # 获取所有父节点的 BO 值
        bo_obs = self.bo  # 形状为 (parent_num,)

        xi_out_obs = 0.7 * self.xi_out_1 + 0.3 * self.xi_out_base # 形状为 (parent_num,)

        # 获取所有父节点下的智能体的平均优先级
        avg_pi_obs = self.avg_pi  # 形状为 (parent_num,)
        for i in range(self.agent_num):
            # 获取智能体与所有父节点的 ETX 值
            etx_obs = self.etx[i]  # 形状为 (parent_num,)

            # 获取智能体的优先级
            pi_obs = self.pi[i]

            # 拼接观测向量
            if self.if_rand_pi:
                obs = np.concatenate([bo_obs, xi_out_obs/12.8, avg_pi_obs, np.array([pi_obs]), self.prev_parent[i]])
                #obs = np.concatenate([xi_out_obs / 12.8, bo_obs,  avg_pi_obs, np.array([pi_obs]), self.prev_parent[i]])
            else:
                obs = np.concatenate([etx_obs, bo_obs, self.prev_parent[i]])

            obs_n.append(obs)

        return obs_n

    def _compute_sending_rates(self):
        """
        计算智能体的最优发送速率
        """
        current_parent = np.argmax(self.current_parent, axis=1)
        self.xi_out = 0.7 * self.xi_out_2 + 0.3 * self.xi_out_1
        pi_inverse = 1.0 / self.pi
        pi_sums = np.bincount(current_parent, weights=pi_inverse, minlength=self.parent_num)
        # 下面为计算的过程
        for i in range(self.agent_num):
            tmp = 1.0 / self.pi[i] / pi_sums[current_parent[i]] * self.xi_out[current_parent[i]]
            self.sending_rates[i] = np.minimum(tmp, self.xi_max[i])

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
            total_rate = np.sum(self.sending_rates[agents_selecting_j] / self.etx[agents_selecting_j, j])
            # 修改了bo的计算方式

            self.bo[j] = total_rate / self.xi_out_1[j]

    def _compute_rewards(self, switch_penalty):
        """
        计算智能体的奖励

        参数:
        - switch_penalty: 一个长度为 agent_num 的数组，表示每个智能体是否切换了父节点

        返回:
        - rewards: 一个长度为 agent_num 的列表，表示每个智能体的奖励
        """

        # 获取每个智能体所选的父节点，形状 (agent_num, )
        parent_idx = np.argmax(self.current_parent, axis=1)

        # ============ 计算 Omega_i 需要的中间量 ============
        # 1) 计算每个父节点下有多少个智能体: n_count[j] = ∑(parent_idx == j)
        n_count = np.bincount(parent_idx, minlength=self.parent_num)  # shape: (parent_num, )
        adjusted_sending_rates = self.sending_rates / self.etx[np.arange(self.agent_num), parent_idx]  # shape: (agent_num, )


        # 2) 计算每个父节点上所有智能体的发送速率之和: parent_sum[j] = ∑(sending_rates[i])，其中 i 属于该父节点
        parent_sum = np.bincount(parent_idx, weights = adjusted_sending_rates, minlength=self.parent_num)  # shape: (parent_num, )

        # 3) numerator[j] = parent_sum[j] + 1
        numerator = parent_sum

        # 4) 为每个智能体映射其对应父节点的 n, numerator, xi_out
        n_parent       = n_count[parent_idx]        # shape: (agent_num, )
        # numerator_par  = numerator[parent_idx]      # shape: (agent_num, )
        # xi_out_par     = self.xi_out[parent_idx]    # shape: (agent_num, )

        # ============ 计算 Omega_i (向量化) ============
        # omega_i[i] = w1 * log(sending_rates[i]+1) 
        #              - w2 * n_parent[i] * ( numerator_par[i] / denominator_par[i] )
        #              - w3 * pi[i] * sending_rates[i]
        omega_i = self.xi_out_1[parent_idx] / self.w5 * self.w1 * np.log(adjusted_sending_rates * self.w5 / self.xi_out_1[parent_idx] + 1.0) \
                - self.w2 * n_parent \
                - self.w3 * (self.pi - self.avg_pi[parent_idx]) * self.sending_rates / self.xi_out_1[parent_idx] \
                - self.w4 * self.sending_rates / self.xi_out_1[parent_idx]            # shape: (agent_num, )
        # omega_i = self.w1 * np.log(adjusted_sending_rates + 1.0) \
        #         - self.w2 * n_parent * (numerator_par / xi_out_par) \
        #         - self.w3 * (self.pi - self.avg_pi[parent_idx]) * self.sending_rates / self.w5 \
        #         - self.w4 * self.sending_rates / self.w5            # shape: (agent_num, )
        # ============ 组合各部分奖励 ============
        # reward_1 = alpha * of1
        # reward_2 = beta * omega_i
        # reward_3 = gamma * switch_penalty
        # reward_1 = self.alpha * of1
        reward_2 = self.beta  * omega_i
        reward_3 = self.gamma * switch_penalty  # shape: (agent_num, )

        # 最终总 reward: reward = reward_1 + reward_2 - reward_3
        final_reward = reward_2 - reward_3  # shape: (agent_num, )

        # ============ 存储到 self.rewards_1/2/3 (如您需要保持原结构) ============
        # self.rewards_1 = reward_1.reshape(-1, 1)  # shape: (agent_num, 1)
        self.rewards_2 = reward_2.reshape(-1, 1)
        self.rewards_3 = reward_3.reshape(-1, 1)

        # 按照原代码的返回格式 (List[List[float]]): [[r0], [r1], ...]
        rewards = final_reward.reshape(-1, 1).tolist()
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
        of1_values = 0.4 * self.etx + 0.73 * self.bo[np.newaxis, :] # 原先是0.6
        
        # 为所有智能体创建切换惩罚矩阵
        prev_parents = np.argmax(self.prev_parent, axis=1)
        switch_penalty = np.ones((self.agent_num, self.parent_num))
        switch_penalty -= self.prev_parent
        
        # 添加切换惩罚
        of1_values += 0.7*switch_penalty
        
        # 找到每个智能体的最优父节点
        best_parents = np.argmin(of1_values, axis=1)
        
        # 创建one-hot编码矩阵
        actions = np.zeros((self.agent_num, self.parent_num))
        actions[np.arange(self.agent_num), best_parents] = 1
        
        return actions
    
    def get_reward(self):
        return self.rewards_2, self.rewards_3
    
    def get_avg_pi(self):
        """
        Calculate and return the average priority (avg_pi) for each parent node.
        Returns:
            float: The average priority value for each parent node.
        """
        # 计算每个父节点的平均优先级
        parent_counts = np.zeros(self.parent_num)
        parent_priorities = np.zeros(self.parent_num)

        current_parent = np.argmax(self.current_parent, axis=1)
        for i in range(self.agent_num):
            parent_idx = current_parent[i]
            parent_counts[parent_idx] += 1
            parent_priorities[parent_idx] += self.pi[i]

        # Avoid division by zero
        parent_counts = np.where(parent_counts == 0, 1, parent_counts)
        self.avg_pi = parent_priorities / parent_counts
        
        return self.avg_pi

    def gray_relational_analysis(self, decision_matrix, current_parent, zeta=0.5):
        """
        Performs Gray Relational Analysis (GRA) for parent selection.

        Args:
            decision_matrix (np.ndarray): The decision matrix (D).
                Rows represent candidate parents (alternatives).
                Columns represent routing metrics (attributes).  Assumes all
                attributes are *cost* attributes (lower values are better).
            zeta (float): The distinguishing coefficient (resolution coefficient).
                Typically between 0 and 1 (default: 0.5).

        Returns:
            int: The index (starting from 0) of the selected parent (alternative)
                with the highest Gray Relational Grade.
        """

        # --- 1. Normalization (Gray Relational Generating) ---
        m, n = decision_matrix.shape  # m: number of parents, n: number of metrics
        normalized_matrix = np.zeros((m, n))

        for j in range(n):
            max_val = np.max(decision_matrix[:, j])
            min_val = np.min(decision_matrix[:, j])

            if max_val == min_val:
                # Handle the case where all values for a metric are the same.
                # Avoid division by zero.  Set normalized values to 0.5.
                #  This essentially neutralizes the metric's impact if it's constant.
                normalized_matrix[:, j] = 0.5
            else:
                normalized_matrix[:, j] = (max_val - decision_matrix[:, j]) / (max_val - min_val)


        # --- 2. Reference Sequence Definition ---
        # x0j = 1 for all j (cost attributes, normalized best value is 1)
        reference_sequence = np.ones(n)

        # --- 3. Gray Relational Coefficient Calculation ---
        gray_coefficients = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                delta_ij = abs(reference_sequence[j] - normalized_matrix[i, j])

                #find min and max delta
                min_delta = np.inf #positive infinity, no delta can be greater than this number
                max_delta = -np.inf #negative infinity, no delta can be smaller than this number
                for k in range(m):
                    for l in range(n):
                        current_delta=abs(reference_sequence[l] - normalized_matrix[k, l])
                        if current_delta<min_delta:
                            min_delta=current_delta
                        if current_delta>max_delta:
                            max_delta=current_delta

                gray_coefficients[i, j] = (min_delta + zeta * max_delta) / (delta_ij + zeta * max_delta)


        # --- 4. Gray Relational Grade Calculation ---
        #  - Weights Calculation (SD Method)
        weights = np.zeros(n)
        for j in range(n):
            mean_j = np.mean(normalized_matrix[:, j])
            std_dev_j = np.std(normalized_matrix[:, j])  #Standard deviation
            weights[j] = std_dev_j

        # Normalize the weights
        sum_weights = np.sum(weights)
        if sum_weights ==0: #Avoid division by zero
            weights=np.ones(n)/n
        else:
            weights = weights / sum_weights


        gray_grades = np.zeros(m)
        for i in range(m):
            gray_grades[i] = np.sum(weights * gray_coefficients[i, :])

        gray_grades += 0.6 * current_parent  # Add a small bonus for the current parent

        # --- 5. Parent Selection (Find parent with highest Gray Relational Grade) ---
        selected_parent_index = np.argmax(gray_grades)  # Index of the best parent

        return selected_parent_index
    
    def OHCA_take_action(self):
        agent_parent_selections = np.zeros(self.agent_num, dtype=int) # To store selected parent index for each agent

        for agent_index in range(self.agent_num):
            # Construct decision matrix for each agent.
            # Here, we are using only ETX as the metric.
            # Decision matrix for agent 'agent_index' will be of shape (parent_num, 1)
            decision_matrix_agent = np.zeros((self.parent_num, 2))
            decision_matrix_agent[:, 0] = self.etx[agent_index, :]  # ETX values (column 1)
            decision_matrix_agent[:, 1] = self.bo[:]               # BO values (column 2) - Assuming same BO for all agents

            current_p = self.current_parent[agent_index]
            # Perform GRA to select the best parent for the current agent
            selected_parent_index = self.gray_relational_analysis(decision_matrix_agent, current_p)
            agent_parent_selections[agent_index] = selected_parent_index

        # Convert parent indices to one-hot encoded actions
        actions = np.zeros((self.agent_num, self.parent_num))
        actions[np.arange(self.agent_num), agent_parent_selections] = 1

        return actions