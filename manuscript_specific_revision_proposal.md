**针对当前十页 ALCC 稿件的具体转投改稿方案**

依据：`Pan_et_al__IJCS (4) (2).pdf`，本文页码均指该 PDF 页码。已核对全文公式和结果叙述，并目视图表。以下是具体修订设计，尚未改动论文源稿、执行新实验或替换研究代码。新实验结果不得当作已取得的结论。

**推荐形成的版本**

保留“解析速率分配＋MAPPO 父节点选择＋切换惩罚”的方法主体，将论文集中在一个问题：节点优先级变化时，如何在吞吐量、按优先级分配的公平性、交付率与父节点切换之间取得可重复的权衡。

保留 ALCC 名称。题目建议为：

*Priority-Aware Rate Allocation and Learning-Based Parent Selection in Wireless Sensor Networks*

采用这个题目，是因为现有证据尚未清楚证明完成了完整 6LoWPAN 协议栈、MAC 和链路重传层面的验证。6LoWPAN 可作为应用背景与模型动机保留；若能回收相应实现证据，则再决定是否保留在标题里。不能只换标题而不修正文中的协议实现和部署主张。

本方案选择保留现有数学结构，通过限定结论、补可证明的性质和有针对性的实验来形成应用研究稿。暂不新增共享容量约束、重造 MAPPO 算法或默认迁移到另一个仿真平台；若新增这些内容，则是另一条需要重新建模的路线。

**第 1–3 页：重写贡献逻辑，而不是只弱化几个形容词**

目前贡献列表分别强调新非合作博弈、稳定 MAPPO 和全面改善性能。建议改成三个可对应证据的贡献：

1. 给出考虑同父节点相对优先级的速率分配规则，并分析固定父节点条件下的唯一解、均衡和优先级单调性。
2. 用 MAPPO 学习父节点选择，以解析分配的速率和优先级信息构造奖励，并引入显式切换惩罚。
3. 比较完整方法、奖励对照、机制消融与原有基线，报告动态优先级下的性能权衡及适用边界。第三条只有在新增实验完成后才写成已完成的贡献。

前两条可采用的英文措辞：

> We formulate a priority-dependent rate-allocation rule and characterize its unique solution for a fixed parent assignment. The analysis clarifies the effect of relative priority on the allocated rate and the conditions under which boundary solutions occur.

> We integrate the analytical rate allocation with a MAPPO-based parent-selection policy. The routing reward uses the allocated rates and relative priorities, together with an explicit penalty for parent changes.

引言按“联合控制已经存在 → 动态优先级下仍需检验哪些具体设计 → 本文比较这些设计”组织。不要用“现有方法不考虑优先级”或“首次联合流量与资源控制”概括创新。OHCA 原文已明确包含混合控制以及节点、应用优先级支持。[OHCA 作者机构库原文](https://eprints.whiterose.ac.uk/id/eprint/121644/7/IEEE_IoT%20Journal_FINAL%20VERSION.pdf)

原稿第 2 页对 Hou 等工作的“lacks generalizability to dynamic settings”需全文或实验支持；未核实前应改成本文要研究的测试问题，不能把没有看到实验等同于算法必然不能适应。最近的 RL 对照优先考察原稿引用的 Hou 等 6LoWPAN 拥塞控制工作，而不是为了容易实现随便选一个不同网络问题的 RL 算法。[作者论文记录](https://faculty.ustc.edu.cn/hehuasen/en/lwcg/233884/content/57543.htm)

建议新增近邻比较表，列：控制动作、优先级如何进入算法、速率与路由的联系、是否有显式切换惩罚、验证场景。每个“无／不支持”都须有依据；未核实写“未核实”，不靠推测填叉号。

**第 3 页 §2.1：网络模型要变得可复现**

保留 sink—intermediate—leaf 的两层结构。压缩泛泛的 DIO/DAO/DIS 教科书描述，把版面留给下列定义：

- 每个叶节点有哪些可选父节点；是全部 3 个，还是存在无线可达性集合。
- 链路成功率、父节点服务率、发送速率的单位与实际含义。
- 仿真控制步对应多少秒；优先级事件何时发生，相对观测、选父节点、算速率和结算交付的顺序。
- Docker 实际承载什么通信；DIO/DAO 是真的收发、只模拟事件，还是仅作概念描述。
- 是否有逐包队列、有限缓冲和重传；若只有流量比率模型，就按该模型描述。

新增一张符号表，把 \(\xi_i\)、\(q_k\)、\(\hat q_k\)、\(\beta_{ik}\)、\(p_i\)、\(\bar p_k\)、\(n_k\)、\(I_i\) 的含义和单位分清。不要继续用一个 \(\xi_{out}\) 同时指真实容量、预测容量和观测容量。

图 1 重画为能对应实验的拓扑，标注节点编号、父节点容量、候选连接与当前连接；图例区分这两种连接。原表 1 与正文的 0 起始／1 起始节点编号需要统一。

**第 4–5 页 §2.2–2.3：保留式（1）–（7），重做解释与证明**

建议统一采用“\(p_i=1\) 为最高优先级，数值越大等级越低”。这是与当前速率公式相容的修订定义，最终必须检查旧实验编码是否一致。

式（15）的公平性对应目标服务权重 \(v_i=1/p_i\)。必须解释这是本文选择的等级到权重映射，而不是任意序数优先级天然等于资源份额。例如等级 1/2/3 映射为 1、1/2、1/3 的相对服务权重。比较 OHCA 等基线时，须按其自身输入定义传递同一语义，不能把本文的“数字越小越重要”直接塞进“数值越大权重越高”的实现。

式（2）和（4）求和改用下标 \(j\)，式（7）的 \(p\) 改为 \(p_i\)。定义

\[
A_i=\omega_2n\beta_i+\omega_3(p_i-\bar p)+\omega_4,\qquad q=\xi_{out}.
\]

新增一个短命题，替代现在只列 KKT 后跳到结论的写法：固定父节点分组、优先级、链路成功率和容量，设 \(q>0\)、\(\omega_1,\omega_5>0\)、\(0<\xi_i^{max}<\infty\)，则每个节点的最优响应唯一，且这些响应构成唯一的固定拓扑速率均衡。

证明只需要：

\[
\frac{\partial F_i}{\partial\xi_i}
=\frac{\omega_1\omega_5}{q+\omega_5\xi_i}-\frac{A_i}{q},\qquad
\frac{\partial^2F_i}{\partial\xi_i^2}
=-\frac{\omega_1\omega_5^2}{(q+\omega_5\xi_i)^2}<0.
\]

严格凹性和紧策略区间给出唯一最优响应；其他节点的速率只出现在加性项中，不改变该最优响应，因此得到本模型特有的均衡唯一性。不要写成“所有严格凹博弈都有唯一均衡”。式（7）的三个分支为：

\[
\xi_i^*=\begin{cases}
0,&A_i\ge\omega_1\omega_5,\\
\xi_i^{max},&A_i\le\dfrac{\omega_1q}{\xi_i^{max}+q/\omega_5},\\
\dfrac{\omega_1q}{A_i}-\dfrac q{\omega_5},&\text{otherwise}.
\end{cases}
\]

这个证明不等于证明父节点切换会收敛，也不等于联合方法在动态优先级下存在全局唯一解。内部解用 clip 的实现还需要检查是否正确覆盖分母非正等边界分支。

可直接加在命题后的英文：

> This equilibrium result applies to a fixed parent assignment and fixed exogenous parameters during a rate-control step. It does not establish convergence of the parent-selection process or guarantee that the aggregate incoming rate remains below the parent service capacity.

增加优先级性质：固定其他节点的优先级，在内部解区间，且 \(\omega_3\ge0\)，

\[
\frac{\partial\xi_i^*}{\partial p_i}
=-\frac{\omega_1q\omega_3(1-1/n)}{A_i^2}\le0.
\]

其中 \(1-1/n\) 不能漏，因为 \(\bar p\) 包含 \(p_i\)。边界上只说非增；只有一个子节点时，相对优先级项恒为零。

原稿下列三段必须删改：

| 位置／当前意思 | 问题 | 替换方向 |
|---|---|---|
| 第 3 页：penalty 是 rigorous constraint，会避免 buffer overflow | 没有共享容量约束 | 明确是软负荷惩罚，超载由指定队列／交付模型处理 |
| 第 4 页：log utility 保障比例公平、低优先级不会饥饿 | \(\log(1+x)\) 与式（7）允许零速率；未证明标准比例公平 | 只说明边际收益递减，公平性与饥饿情况由指标评估 |
| 第 4 页：平均优先级上升会抑制发送、避免 channel collapse | 不符合 \(p_i-\bar p\) 的数学行为 | 改成同父节点下相对等级的差异化机制 |

尤其应明确：固定分组时，所有等级同时加同一个数，\(p_i-\bar p\) 不变，速率规则不变。这个性质只涉及速率分配，不意味着观察绝对等级的 MAPPO 路由策略也不变。

保留软惩罚的依据是改动小且数学自洽；不能继续保留容量保证。反例可以在内部验证或附录给出：论文参数、容量 12.8、3 个节点、\(\beta_i=1\)、等级 [1,3,3] 时，速率约 [7.9497,3.0805,3.0805]，和为 14.1106，超过容量。

**第 5–6 页 §3：把奖励与算法写成实际实现的机制**

式（8）保留现有设计方向，明确它是 surrogate，删除“直接代入式（4）均衡收益”以及“因此保证最大化网络 social welfare”的推断。建议在公式前放：

> The parent-selection reward is a game-informed surrogate evaluated using the rate allocation in Equation (7). It differs from the traffic-control payoff in Equation (4): the utility is rescaled and the aggregate-load penalty is replaced by a parent-occupancy penalty.

公式后放：

> The occupancy term depends on the number of children assigned to the selected parent. It discourages concentration of nodes but does not enforce a capacity constraint. The benefit of this reward design is evaluated against a generic performance-based reward using the same policy architecture and training budget.

第二段最后一句在对应实验完成后才能放入最终稿。删掉“为了降低计算复杂度且保持原拥塞代价本质”的现有解释，因为原稿没有证明这两点。

式（9）改写为清楚的时序：

\[
R_i(t)=\widetilde F_i(t)-c\,\mathbf 1\{a_i(t)\ne I_i(t)\},
\]

其中 \(I_i(t)\) 是决策前父节点，\(a_i(t)\) 是本次选择；首次建立连接是否计费需明确。避免使用未清楚定义的 \(\delta(t)\)。这项惩罚只能先称为减少切换的设计，不能在没有测量时直接称为节能或减少真实控制报文开销。

式（12）目前是联合动作概率比，而 Algorithm 1 使用逐智能体概率比，应统一为

\[
\rho_{t,i}(\theta)=\frac{\pi_\theta(a_i(t)\mid o_i(t))}{\pi_{\theta_{old}}(a_i(t)\mid o_i(t))}.
\]

式（11）的 advantage、式（13）的 return 和 Algorithm 1 必须与实际 reward 聚合一致。当前所查代码传递的是个体 reward，不能直接写成先求和得到团队 reward 再训练。最快的处理是准确描述最终采用的训练实现，去掉未经实现的共享收益最优化保证；如果选择改成团队奖励，需明确这是算法变动，并重新训练所有相关组。

第 7 页“Actor 与 Critic 都接 softmax”要改：actor 输出离散父节点选择分布；所查 critic 为标量 value 输出。第 5 页列入 actor 的 ETX 与代码常用观测分支不一致，同样先确定最终实现，再同时改状态定义、图 2 和参数表。

图 2 改为跨双栏结构，明确“观测 → actor → 父节点选择 → 重新统计父节点子节点与平均等级 → 式（7）速率分配 → 链路／交付反馈 → reward”。训练路径与推理路径分开，避免将所有标准 MAPPO 细节都塞进单栏小图。

Algorithm 1 主文保留上述问题专属步骤及训练数据流，标准 PPO 细节可移附录。无须通过更复杂的神经网络结构制造新贡献。

**第 5–7 页：复杂度与容量预测的两项低成本纠错**

删除第 5 页 \(O(H^L)\)，保留第 6 页稠密网络前向计算量：

\[
O(d_{in}H+(L-1)H^2+HM).
\]

速率求解的 \(O(1)\) 限于已获得父节点统计量时的每节点计算；父节点统计子节点数量、平均等级等仍有聚合开销。固定架构计算量固定不代表已验证能部署于受限传感器；无设备测试时不写实时资源消耗保证。

式（14）若确实想表达两次观测的加权预测，可改符号为

\[
\hat q_k(t+1)=\eta y_k(t)+(1-\eta)y_k(t-1),
\]

并称 two-sample weighted predictor。它与标准单指数平滑递推不同。若改成用上一次预测值的递推式，则改变算法，需要重跑。当前代码还对观测和速率求解使用不同的加权比例，不能用一个 \(\eta\) 模糊带过；必须决定最终到底使用哪一种，并据实描述。

**第 7–9 页 §4：按三个研究问题重排实验**

RQ1：ALCC 是否改变吞吐量、公平性和交付率的权衡？对应原图 3、表 2。

RQ2：优先级项、所提 reward 与切换惩罚各自贡献了什么？对应新增机制消融及改造后的图 4。

RQ3：优先级变化加快、同时变化的节点增加和负载升高时，结论还成立吗？对应新增动态与压力测试。

§4.1 不应只详述 DIO／DAO 流程。改成实际运行平台、节点／链路模型、事件更新次序、训练与测试分离、基线适配及指标定义。使用 Docker 这一事实不能替代对 MAC／队列／重传模型的说明。

**原图 3 与表 2：先统一数据，再讨论提升幅度。** 第 8 页图 3(c)目视 OHCA WFI 约 0.79–0.80、ALCC 约 0.94–0.95，对应比值约 0.84；第 9 页表 2 却写 OHCA=0.9108。这是需要核对的明显差异，不能仅靠补一个置信区间解决。图上估计不是精确数据，最后应以可追溯原始输出为准。检查是否用了不同运行版本、时间窗口、优先级设定或聚合方式。

建议表 2 完全重做为：方法、吞吐量原单位、WFI、PDR、切换频率，各报告均值和合适的不确定性；归一化放附录。此前由表 2 换算出的“吞吐量提高 2.47%、WFI 提高 9.79%”只是表内算术结果，在数据一致性解决前不能直接作为新稿摘要数字。

图 3 保留三个指标，增加通用奖励 MAPPO 对照及独立运行不确定性，标明事件时间和统计区间。图注去掉“superior behavior”：原图中 OHCA 的 PDR 明显高于 ALCC。对原正文的“低 0.4%”核对究竟是相对百分比还是百分点。

**表 1：移附录，取消因果证明用途。** 单个 500 秒的节点连接快照只能解释策略例子，不能证明父节点分配最优或 WFI 增益原因。若保留，增加父节点容量、有效到达率和负载率，并标明是代表性场景；不要据一张表写“directly attributable”。

**图 4：增加真正的稳定性指标。** 现图只有 throughput、WFI、PDR，不能证明减少 route flapping。主文改为随 \(c\) 的汇总曲线，至少包含每节点单位控制步的切换次数；保留原三项性能作为代价。原来的七组时间曲线可移附录，注明阴影到底是什么。

\(c=1\) 不写成普遍合理或最优。用验证集上的预定规则选择，或者只将它列为一组权衡结果；测试集用于报告，不用于挑选 \(c\)。若比较的是惩罚对学习策略的作用，每个 \(c\) 必须匹配相应训练，不能在冻结模型上只改 reward 系数。

**新增实验的具体配置与解释**

| 实验 | 对这篇稿件的具体操作 | 输出 | 能支持什么 |
|---|---|---|---|
| 固定父节点的优先级检查 | 保留原参数；在相同容量和链路下改变一个节点等级，并更新均值；检查边界分支 | 等级—发送率曲线、各等级交付率 | 式（7）的优先级解释和数值实现正确 |
| 速率优先级项消融 | 仅在式（4）／（7）关闭 \(\omega_3(p_i-\bar p)\)，保留 \(\omega_4\)、actor 观测和原 reward 结构 | 原单位吞吐、WFI、按等级指标 | 相对优先级在速率分配中的作用；不能叫完全无优先级 |
| reward 对照 | 同一个 MAPPO、同一速率规则，用预定义归一化吞吐／公平性奖励并保留相同切换惩罚 | 主结果与独立训练变异 | 所提 surrogate 是否比一般性能奖励更有帮助 |
| 切换消融 | 完整 ALCC 与从头训练的 \(c=0\) 比较 | 切换频率＋吞吐／公平／PDR | 减少切换是否带来可测量权衡 |
| 更快变化 | 原 100 秒单节点场景，加 20 秒单节点及 20 秒多节点事件；若没有秒映射，则统一采用控制步 | 事件对齐的按等级性能与恢复曲线 | 动态变化的适应性，区分频率和影响节点数 |
| 负载压力 | 从 10 叶节点扩到 30，保留 3 个父节点及容量，明确这同时改变争用负载 | 三指标和各等级服务 | 固定容量下的负载承受边界；不是任意拓扑泛化 |

优先级变化不等于真实业务突发：如果模型没有外生数据到达过程，就只称“priority-change events”，删除“模拟节点退出加入”和“突发包流量”的等同表达。若需要宣称处理突发流量，应另定义并实际改变业务到达率，不能仅改变优先级标签。

固定父节点的解析检查无需训练。完整 ALCC、优先级项消融、通用奖励、无切换惩罚四个学习组需独立训练；OHCA、NGECC 在同一外部场景重新评估。建议至少三个独立训练 seed，条件允许用五个，测试 episode 的重复不能替代训练重复。

相近 RL 文献比较：优先核查 Hou 等 2023 工作的全文与实现。无法按原定义复现时，不用一个普通 DQN 冒名替代；可以先完成上述内部 MAPPO 对照并缩小外部性能主张，但最近 RL 基线缺失仍是下一轮可能提出的问题。

**统计和复现具体写法**

保留逐 episode 的原始结果和测试场景，分开记录 training seed 与 scenario seed。主指标采用预先规定的完整测试窗口；如果同时给稳态指标，另外定义 burn-in，并对所有方法保持一致。

训练曲线优先展示各方法共同的验证性能随训练步数变化，而不是直接比较不同尺度的训练 reward。报告学习率、层数／宽度、优化器、PPO clip、GAE、折扣、batch／minibatch、更新次数、环境步数、停止／checkpoint 选择规则、设备与训练耗时，全部使用实际运行值。

若仅有三个训练 seed，明确跨训练随机性的证据有限，展示各 seed 结果。对同一 checkpoint 的 500 次环境测试所得区间只能描述该模型的条件测试不确定性；不要把这些测试当成 500 个独立训练模型。

**第 1 页摘要与第 9 页结论：等图表核准后统一替换**

摘要的前半段可以先改成：

> Changing traffic priorities introduce trade-offs between throughput, service differentiation, and routing stability in sensor networks. We present ALCC, which combines an analytical priority-dependent rate-allocation rule with MAPPO-based parent selection. A switching penalty is included in the routing reward to control the frequency of parent changes.

后半段只写已完成的实验设置与核准后的结果：相对哪些方法、什么指标提高多少、PDR 有何代价，以及当前模型没有验证哪些协议机制。不要现在把旧表的提升幅度填入这个版本。

结论收束为三点：在已测试条件下取得的权衡；消融实际支持的设计作用；抽象网络模型和训练泛化的限制。删除“保证全局最优”“完全避免饥饿／拥塞”及未测得的节能、控制开销减少。只在真实测量支持时使用这些表达。

**最终稿的版面结构建议**

| 章节 | 内容 | 对应证据 |
|---|---|---|
| 1 Introduction | 具体问题、近邻方法及三项限定贡献 | 相关工作差异表 |
| 2 System Model and Priority-Dependent Rate Allocation | 网络假设、优先级定义、式（1）–（7）、短命题 | 拓扑图、参数与符号表、优先级检查 |
| 3 Learning-Based Parent Selection | 状态／动作、surrogate reward、切换项、准确训练过程 | 重画图 2、精简 Algorithm 1 |
| 4 Evaluation | 主比较、机制消融、动态变化与压力测试 | 原单位主表、重画图 3／4、新动态图、训练曲线 |
| 5 Limitations and Conclusion | 支持的结论与明确边界 | 与结果逐项一致 |

原表 1 节点快照、七条 \(c\) 的完整时间曲线、通用 PPO 推导可移附录。由此腾出主文空间容纳新增实证，无需靠无限增加篇幅处理审稿意见。

本方案的完成标志是：固定拓扑速率理论正确、方法描述与实现一致、优先级变化真实生效、图 3／表 2 数据一致、关键机制有消融证据、性能代价在摘要和结论中如实呈现。满足这些条件后，再按目标期刊格式转换。
