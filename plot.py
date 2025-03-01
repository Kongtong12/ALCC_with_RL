import numpy as np
import matplotlib.pyplot as plt

# 定义算法和指标
algorithms = ['RL', 'NGECC', 'OHCA']
metrics = ['WFI', 'throughput', 'ratio']

# 加载九个 .npy 文件的数据
data = {}
for algo in algorithms:
    for metric in metrics:
        filename = f'{algo}_{metric}.npy'
        try:
            data[(algo, metric)] = np.load(filename)
        except FileNotFoundError:
            print(f"警告：文件 {filename} 未找到，跳过该文件。")

# 为每个指标绘制一张图
for metric in metrics:
    plt.figure()  # 创建新的图形
    for algo in algorithms:
        if (algo, metric) in data:
            plt.plot(data[(algo, metric)], label=algo)
    plt.title(f'{metric} 对比图')  # 图表标题
    plt.xlabel('索引')  # x轴标签，可根据数据含义调整
    plt.ylabel(metric)  # y轴标签
    plt.legend()  # 添加图例
    plt.savefig(f'{metric}_plot.png')  # 保存为 PNG 文件
    plt.close()  # 关闭图形以释放内存

print("绘图完成，已生成 WFI_plot.png, throughput_plot.png 和 ratio_plot.png。")