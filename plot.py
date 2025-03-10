import numpy as np
import matplotlib.pyplot as plt

# 定义算法和指标
algorithms = ['RL', 'NGECC', 'OHCA']
metrics = ['WFI', 'throughput', 'ratio']

# 定义每个算法的线条样式、颜色和标记
line_styles = {
    'RL': {'linestyle': '-', 'color': 'blue', 'marker': 's', 'markersize': 8},      # 蓝色实线，方形标记
    'NGECC': {'linestyle': '--', 'color': 'red', 'marker': 'o', 'markersize': 8},   # 红色虚线，圆形标记
    'OHCA': {'linestyle': '-.', 'color': 'green', 'marker': '^', 'markersize': 8}   # 绿色点划线，三角形标记
}

# 加载九个 .npy 文件的数据
data = {}
for algo in algorithms:
    for metric in metrics:
        filename = f'{algo}_{metric}.npy'
        try:
            data[(algo, metric)] = np.load(filename)
        except FileNotFoundError:
            print(f"警告：文件 {filename} 未找到，跳过该文件。")

# 创建新的时间尺度：0到1000之间均匀分布的20个点
new_time_scale = np.linspace(0, 1000, 21)

# 为每个指标绘制一张图
for metric in metrics:
    plt.figure(figsize=(10, 6))  # 创建新的图形，设置更大的尺寸
    for algo in algorithms:
        if (algo, metric) in data:
            # 原始数据（假设有200个点）
            original_data = data[(algo, metric)]
            
            # 如果原始数据确实有200个点
            if len(original_data) == 200:
                # 创建原始数据的索引（0到199）
                original_indices = np.linspace(0, 199, 200)
                
                # 重采样到20个点
                # 使用线性插值获取新时间尺度下的数据点
                resampled_data = np.interp(
                    np.linspace(0, 199, 21),  # 在原始索引范围内均匀选择20个点
                    original_indices,
                    original_data
                )
                
                # 使用新的时间尺度和重采样的数据进行绘图，添加标记和样式
                plt.plot(new_time_scale, resampled_data, label=algo, **line_styles[algo])
            else:
                # 如果原始数据点数不是200，则进行通用重采样
                original_indices = np.linspace(0, len(original_data)-1, len(original_data))
                resampled_data = np.interp(
                    np.linspace(0, len(original_data)-1, 21),
                    original_indices,
                    original_data
                )
                plt.plot(new_time_scale, resampled_data, label=algo, **line_styles[algo])
    
    # 设置更细致的刻度
    plt.xticks(np.linspace(0, 1000, 11))  # x轴上设置11个标记点（0, 100, 200, ..., 1000）
    
    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.title(f'{metric}', fontsize=14)  # 图表标题，增大字体
    plt.xlabel('Time', fontsize=12)  # x轴标签
    plt.ylabel(metric, fontsize=12)  # y轴标签
    
    # 添加图例，并设置在图表外部右上方
    plt.legend(loc='upper right', fontsize=10, framealpha=0.8)
    
    # 调整布局，确保所有元素都显示完整
    plt.tight_layout()
    
    plt.savefig(f'{metric}_plot.png', dpi=300)  # 保存为高分辨率PNG文件
    plt.close()  # 关闭图形以释放内存

print("绘图完成，已生成 WFI_plot.png, throughput_plot.png 和 ratio_plot.png。")