# Neural Cleanse 检测难度说明

## 1. 检测方法说明

本项目采用简化版 Neural Cleanse 思路评估不同触发器位置的检测难度。完整 Neural Cleanse 通常需要反向优化触发器掩码，并比较不同类别恢复出的触发器大小。本项目时间和计算资源有限，因此使用 `source_code/defense/detection_score.py` 中实现的简化指标：

```text
Detection Score = 给测试样本添加指定位置触发器后，模型预测为目标类别 0 的平均置信度
```

该指标用于衡量触发器对目标类别的激活强度。Detection Score 越高，说明模型在看到该位置触发器后越容易被激活到目标类别，触发器特征越明显，因此检测难度越低；Detection Score 越低，说明触发器激活目标类别的平均置信度相对较弱，检测难度相对更高。

Mask Norm 使用固定 3x3 触发器在 32x32 图像中的面积占比计算：

```text
Mask Norm = 3 * 3 / (32 * 32) = 0.008789
```

因为 9 个位置使用完全相同大小的白色方块触发器，所以 Mask Norm 在不同位置之间保持一致。本实验中的位置差异主要由 Detection Score 反映。

## 2. 检测难度判定规则

代码中使用以下规则划分 Detection Difficulty：

<p align="center">表 1 Detection Difficulty 判定规则</p>

| Detection Score 范围 | Detection Difficulty |
|---:|---|
| score >= 0.80 | Low Detection Difficulty |
| 0.50 <= score < 0.80 | Medium Detection Difficulty |
| score < 0.50 | High Detection Difficulty |

因此，Detection Score 越高，表示越容易被检测；Detection Difficulty 中的 Low 表示检测难度低，不表示攻击风险低。

## 3. 检测结果汇总

<p align="center">表 2 不同触发器位置下的检测结果</p>

| Position | Detection Score | Mask Norm | Detection Difficulty |
|---|---:|---:|---|
| top_left | 0.929033 | 0.008789 | Low Detection Difficulty |
| top_center | 0.952519 | 0.008789 | Low Detection Difficulty |
| top_right | 0.930278 | 0.008789 | Low Detection Difficulty |
| middle_left | 0.973748 | 0.008789 | Low Detection Difficulty |
| center | 0.980641 | 0.008789 | Low Detection Difficulty |
| middle_right | 0.980572 | 0.008789 | Low Detection Difficulty |
| bottom_left | 0.968406 | 0.008789 | Low Detection Difficulty |
| bottom_center | 0.975373 | 0.008789 | Low Detection Difficulty |
| bottom_right | 0.967315 | 0.008789 | Low Detection Difficulty |

## 4. 结果分析

从检测结果看，9 个位置的 Detection Score 均高于 0.92，全部被划分为 Low Detection Difficulty。这说明在本实验设定下，3x3 白色方块触发器对目标类别具有明显激活效果，简化检测指标能够比较容易地观察到后门行为。

按 Detection Score 从高到低排序，最容易被检测的位置依次为 center、middle_right、bottom_center、middle_left。这些位置的分数均接近或超过 0.974，说明模型对这些空间区域中的触发器响应更强。相对而言，top_left 和 top_right 的 Detection Score 最低，分别为 0.929033 和 0.930278，但二者仍然明显高于 0.80 阈值，因此不能认为它们具有高检测难度，只能说在 9 个位置中相对不那么显著。

综合来看，触发器位于图像中部或偏下区域时，模型对目标类别的平均置信度更高，检测更容易；触发器位于顶部角落时，检测分数相对较低，但仍属于容易检测范围。

## 5. 可写入报告的结论

本实验基于简化 Neural Cleanse 思想，使用添加触发器后模型预测目标类别的平均置信度作为 Detection Score。结果显示，9 个触发器位置的 Detection Score 均处于较高水平，说明固定 3x3 白色触发器在不同空间位置下都能明显激活目标类别，整体检测难度较低。其中 center、middle_right、bottom_center 等位置检测分数最高，表明这些位置的后门特征最容易被检测；top_left 和 top_right 的检测分数相对较低，但仍高于低检测难度阈值。因此，在本实验设置下，触发器位置会影响检测分数大小，但尚未形成从“容易检测”到“难以检测”的显著等级差异。
