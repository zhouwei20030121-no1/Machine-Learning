# Neural Cleanse 检测难度分析

## 1. 检测方法说明

本项目采用的是简化版 Neural Cleanse 思路，不是完整的反向优化触发器流程。具体做法是：对 CIFAR-10 测试集样本加入对应位置的 3x3 白色触发器，然后输入已经训练好的后门模型，统计模型预测为目标类别 0 的平均置信度，记为 Detection Score。

Detection Score 越高，说明触发器越容易激活模型输出目标类别 0，后门特征越明显；Detection Score 越低，说明触发器激活效果越弱，相对更不容易被当前检测方法发现。

Mask Norm 表示触发器区域面积占整张图片面积的比例。本实验中触发器大小为 3x3，CIFAR-10 图片大小为 32x32，因此：

```text
Mask Norm = 3 * 3 / (32 * 32) = 0.008789
```

## 2. 检测结果

<p align="center">表 1 不同触发器位置下 Detection Score 检测结果</p>

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

## 3. 结果分析

9 个触发器位置的 Detection Score 均高于 0.92，并且全部被划分为 Low Detection Difficulty。这说明在当前实验设置下，3x3 白色触发器能够非常明显地激活后门模型对目标类别 0 的响应，后门特征整体比较显著。

Detection Score 最高的位置是 center，分数为 0.980641；其次是 middle_right，分数为 0.980572。这两个位置的触发器激活效果最强，但也最容易被当前检测方法发现。

Detection Score 最低的位置是 top_left，分数为 0.929033；其次是 top_right，分数为 0.930278。它们相对更隐蔽，但分数仍然高于 0.92，因此不能认为是真正难以检测，只能说在 9 个位置中相对检测显著性较低。

## 4. 可直接放入报告的文字

本文使用简化版 Neural Cleanse 检测方法对 9 个触发器位置对应的后门模型进行检测。检测时，在 CIFAR-10 测试集样本中加入对应位置的 3x3 白色触发器，并统计模型预测为目标类别 0 的平均置信度，作为 Detection Score。实验结果显示，9 个位置的 Detection Score 均高于 0.92，并全部属于 Low Detection Difficulty。这说明当前实验中的后门触发器对目标类别具有明显激活效果，后门特征较容易被检测出来。

从空间位置看，center 和 middle_right 的 Detection Score 最高，说明这两个位置的触发器最容易激活后门，同时也最容易被发现；top_left 和 top_right 的 Detection Score 相对最低，说明它们在本实验中相对更隐蔽，但由于检测分数仍然较高，不能认为其具备强隐蔽性。
