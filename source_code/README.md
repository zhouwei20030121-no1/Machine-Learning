# CIFAR-10 后门攻击触发器位置敏感性分析代码框架

本目录用于课程设计代码实现，默认实验设置与任务分工文档保持一致：

- 数据集：CIFAR-10
- 攻击方法：BadNets
- 触发器：3x3 白色方块
- 触发器位置：3x3 九个空间位置
- 目标类别：0
- 投毒比例：0.10
- 随机种子：2026
- 评价指标：Clean Accuracy、ASR、Detection Score、Mask Norm、Detection Difficulty

## 目录结构

```text
source_code/
  models/cnn_model.py                 # Simple CNN 模型
  utils/config.py                      # 统一实验参数和路径
  utils/trigger_utils.py               # 触发器添加函数
  utils/dataset_poison.py              # BadNets 投毒数据集包装
  experiments/train_backdoor.py        # 单位置后门模型训练
  experiments/evaluate_clean_acc.py    # 干净准确率测试
  experiments/evaluate_asr.py          # ASR 测试
  experiments/run_position.py          # 单位置训练 + 测试 + 写 CSV
  experiments/run_poison_rate_ablation.py
  defense/detection_score.py           # 简化 Neural Cleanse 检测分数
  analysis/merge_results.py            # 合并 part1/part2/检测结果
  analysis/plot_results.py             # 基础图表生成
  analysis/visualize_trigger_samples.py
  results/csv/
  results/models/
  results/logs/
  figures/
  test_data/
```

## 环境安装

```bash
cd source_code
pip install -r requirements.txt
```

第一次运行会自动下载 CIFAR-10 到 `source_code/data/`。

## 跑单个触发器位置

从 `source_code` 目录运行：

```bash
python -m experiments.run_position --position top_left --part part1
```

李卓尔负责的位置：

```bash
python -m experiments.run_position --position top_left --part part1
python -m experiments.run_position --position top_center --part part1
python -m experiments.run_position --position top_right --part part1
python -m experiments.run_position --position middle_left --part part1
python -m experiments.run_position --position center --part part1
```

贾思楠负责的位置：

```bash
python -m experiments.run_position --position middle_right --part part2
python -m experiments.run_position --position bottom_left --part part2
python -m experiments.run_position --position bottom_center --part part2
python -m experiments.run_position --position bottom_right --part part2
```

输出：

- `results/csv/asr_acc_results_part1.csv`
- `results/csv/asr_acc_results_part2.csv`
- `results/models/backdoor_<position>.pt`

## 防御检测

```bash
python -m defense.detection_score --position top_left --model-path results/models/backdoor_top_left.pt
```

输出默认追加到：

```text
results/csv/detection_results.csv
```

## 合并最终结果

```bash
python -m analysis.merge_results
```

输出：

```text
results/csv/final_results.csv
```

最终结果表会包含：

- Position
- Clean Accuracy
- ASR
- Detection Score
- Mask Norm
- Detection Difficulty
- Tradeoff Type

## 生成基础图表

```bash
python -m analysis.plot_results
python -m analysis.visualize_trigger_samples
```

输出在 `figures/` 下，包括 ASR 热力图、检测难度热力图、准确率对比图、ASR 与检测难度权衡图、触发器样本九宫格。

## 投毒比例消融实验

```bash
python -m experiments.run_poison_rate_ablation --position bottom_right --rates 0.05 0.10 0.15
```

输出：

```text
results/csv/poison_rate_ablation.csv
```

