import numpy as np
from tqdm import tqdm

def generate_data():
    """
    生成 100 组节点数据：
      - 2 节点：10 组
      - 3 节点：60 组
      - 4 节点：30 组
    每组随机生成优先级 p_i ∈ {1, 2, 3}
    返回一个列表 data_sets，长度为 100，每个元素为 (n, p_array)
    """
    data_sets = []

    # 2 节点，10 组
    for _ in range(10):
        n = 2
        p = np.random.randint(1, 4, size=n)  # p ∈ {1,2,3}
        data_sets.append((n, p))

    # 3 节点，60 组
    for _ in range(60):
        n = 3
        p = np.random.randint(1, 4, size=n)
        data_sets.append((n, p))

    # 4 节点，30 组
    for _ in range(30):
        n = 4
        p = np.random.randint(1, 4, size=n)
        data_sets.append((n, p))

    return data_sets

def compute_sending_rates(n, p_array, w1, w2, w3, w4, xi_out, sigma):
    """
    根据给定的 n, p_array，以及参数 w1, w2, w3, w4, xi_out, sigma，
    计算该组节点的所有 sending_rate(i)，并返回对应的数组。

    公式:
    sending_rate(i) = -1 + w1 * xi_out / (w2 * n * sigma
                                         + w3 * (p_i - avg_p) * xi_out
                                         + w4 * xi_out)
    """
    avg_p = np.mean(p_array)
    
    # 不随 p_i 变化的分母部分
    denominator_base = w2 * n * sigma + w4 * xi_out

    sending_rates = []
    for p_i in p_array:
        denominator = denominator_base + w3 * (p_i - avg_p) * xi_out
        rate = -1 + w1 * xi_out / denominator
        sending_rates.append(rate)
    
    return np.array(sending_rates)

def compute_metrics_for_params(w2, w3, w4, data_sets, w1, xi_out, sigma, m):
    """
    功能：给定 w2, w3, w4，计算并返回以下四个量：
      1) 100 组节点数据的 平均 Throughput
      2) 混合所有节点数据时的 WFI
      3) 100 组中最大的 (sum(sending_rate)*sigma / xi_out)
      4) 100 组 Throughput 的方差

    参数:
      - w2, w3, w4: 待搜索的参数
      - data_sets:  之前生成的 100 组节点数据, 格式 [(n, p_array), ...]
      - w1, xi_out, sigma, m: 其他固定参数，m 为 100 组节点的总数 (320)

    返回:
      (avg_throughput, wfi, max_ratio, var_throughput)
    """
    throughput_list = []
    srp_all = []            # sending_rate(i) * p_i
    srp_square_all = []     # (sending_rate(i)*p_i)^2
    ratio_list = []         # (sum(sending_rate)*sigma / xi_out) 各组的值

    for (n, p_array) in data_sets:
        # 计算该组下的 sending_rate
        sr = compute_sending_rates(n, p_array, w1, w2, w3, w4, xi_out, sigma)
        sum_sr = np.sum(sr)

        # throughput
        throughput_list.append(sum_sr * sigma)

        # WFI 需要 sending_rate(i)*p_i
        srp = sr * p_array
        srp_all.extend(srp)
        srp_square_all.extend((srp)**2)  # (sending_rate(i)*p_i)^2

        # ratio
        ratio_list.append((sum_sr * sigma) / xi_out)

    # (1) 平均 Throughput
    avg_throughput = np.mean(throughput_list)

    # (2) WFI
    srp_all = np.array(srp_all)
    srp_square_all = np.array(srp_square_all)
    numerator = (np.sum(srp_all))**2
    denominator = m * np.sum(srp_square_all)
    wfi = numerator / denominator if denominator != 0 else 0.0

    # (3) max_ratio
    max_ratio = np.max(ratio_list)

    # (4) 100 组 Throughput 的方差
    var_throughput = np.var(throughput_list)

    return (avg_throughput, wfi, max_ratio, var_throughput)

def compute_matrix_for_w2(w2, w3_values, w4_values, data_sets, w1, xi_out, sigma, m):
    """
    在固定 w2 的情况下，以 w3, w4 为横纵坐标，构造一个矩阵，
    每个元素为 (avg_throughput, wfi, max_ratio, var_throughput)

    参数:
      - w2: 固定参数
      - w3_values, w4_values: w3, w4 循环取值列表
      - data_sets:  100 组节点数据
      - w1, xi_out, sigma, m: 其余固定参数
    
    返回:
      一个二维 list，形状 (len(w3_values), len(w4_values))，
      每个元素为 (avg_throughput, wfi, max_ratio, var_throughput)
    """
    matrix_result = []

    for w3 in w3_values:
        row_result = []
        for w4 in w4_values:
            metrics = compute_metrics_for_params(
                w2, w3, w4, data_sets, w1, xi_out, sigma, m
            )
            row_result.append(metrics)
        matrix_result.append(row_result)

    return matrix_result

def main():
    # 固定参数
    xi_out = 12.8
    sigma = 0.95
    w1 = 15
    m = 2*10 + 3*60 + 4*30  # 总节点数 320

    # 生成 100 组数据
    data_sets = generate_data()

    # 示例：搜索范围
    w2_values = np.arange(6, 12.1, 0.5)
    w3_values = np.arange(0.8, 3.1, 0.2)
    w4_values = np.arange(0.2, 2.1, 0.2)

    # ============ 1) 演示：查看某一个 (w2, w3, w4) 的四项指标 ============
    example_w2 = 8.0
    example_w3 = 2.0
    example_w4 = 1.0
    example_metrics = compute_metrics_for_params(
        example_w2, example_w3, example_w4, 
        data_sets, w1, xi_out, sigma, m
    )
    print(f"[单次调用] 对参数 (w2={example_w2}, w3={example_w3}, w4={example_w4}) 的四项指标：")
    print("  平均Throughput =", example_metrics[0])
    print("  WFI           =", example_metrics[1])
    print("  最大 ratio    =", example_metrics[2])
    print("  Throughput方差 =", example_metrics[3])
    print()

    # ============ 2) 演示：固定 w2，计算 (w3, w4) 网格 => 四项指标矩阵 ============
    fixed_w2 = 8.0
    matrix_result = compute_matrix_for_w2(
        fixed_w2, w3_values, w4_values,
        data_sets, w1, xi_out, sigma, m
    )

    # matrix_result 是一个二维 list，
    # 大小为 [len(w3_values)][len(w4_values)]，
    # 每个元素为 (avg_throughput, wfi, max_ratio, var_throughput)
    print(f"[矩阵] 固定 w2={fixed_w2}，行列分别对应 w3, w4:")
    # 这里演示只查看前 2 行、前 2 列
    for i in range(2):
        for j in range(2):
            # (avg_throughput, wfi, max_ratio, var_throughput)
            print(f"w3={w3_values[i]}, w4={w4_values[j]} => {matrix_result[i][j]}")
        print()

    # ============ 3) 如果仍需遍历全部 w2, w3, w4, 可像之前一样做 ============ 
    print("开始三层循环搜索 (演示) ...")
    results = []
    for w2 in tqdm(w2_values, desc="Loop over w2"):
        for w3 in tqdm(w3_values, desc="Loop over w3", leave=False):
            for w4 in w4_values:
                avg_throughput, wfi, max_ratio, var_throughput = compute_metrics_for_params(
                    w2, w3, w4, data_sets, w1, xi_out, sigma, m
                )
                results.append((w2, w3, w4, avg_throughput, wfi, max_ratio, var_throughput))

    print("搜索完成，总结果数量：", len(results))
    # 示范查看前 3 条结果
    for i in range(3):
        print(f"{i} => w2={results[i][0]:.2f}, w3={results[i][1]:.2f}, w4={results[i][2]:.2f}, "
              f"Throughput={results[i][3]:.4f}, WFI={results[i][4]:.4f}, MaxRatio={results[i][5]:.4f}, Var={results[i][6]:.4f}")


if __name__ == "__main__":
    main()
