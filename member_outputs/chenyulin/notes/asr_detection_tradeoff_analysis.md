# ASR 与检测难度权衡分析

## 1. 分析目标

本部分结合 Attack Success Rate 和 Detection Score，分析不同触发器位置在攻击有效性和隐蔽性之间的关系。理想情况下，如果某个位置同时具有较高 ASR 和较低 Detection Score，可以认为该位置具有更高隐蔽风险；如果 ASR 高但 Detection Score 也高，则说明攻击有效，但后门特征也更明显。

本实验中 ASR 来自前序同学的 9 个位置主实验结果，Detection Score 来自 `source_code/defense/detection_score.py` 的检测输出。

## 2. 联合结果表

<p align="center">表 1 ASR 与 Detection Score 联合分析结果</p>

| Position | Clean Accuracy | ASR | Detection Score | Detection Difficulty |
|---|---:|---:|---:|---|
| top_left | 0.7642 | 0.9298 | 0.929033 | Low Detection Difficulty |
| top_center | 0.7261 | 0.9535 | 0.952519 | Low Detection Difficulty |
| top_right | 0.7122 | 0.9310 | 0.930278 | Low Detection Difficulty |
| middle_left | 0.7639 | 0.9747 | 0.973748 | Low Detection Difficulty |
| center | 0.7675 | 0.9817 | 0.980641 | Low Detection Difficulty |
| middle_right | 0.7240 | 0.9820 | 0.980572 | Low Detection Difficulty |
| bottom_left | 0.7210 | 0.9704 | 0.968406 | Low Detection Difficulty |
| bottom_center | 0.7591 | 0.9764 | 0.975373 | Low Detection Difficulty |
| bottom_right | 0.7515 | 0.9688 | 0.967315 | Low Detection Difficulty |

## 3. 权衡关系观察

从整体趋势看，ASR 与 Detection Score 呈高度一致关系。ASR 较高的位置通常也具有较高的 Detection Score，例如 center、middle_right、bottom_center、middle_left 的 ASR 均高于 0.974，Detection Score 也都高于 0.973。这说明这些位置的触发器不仅攻击成功率高，也更容易被简化检测指标捕捉到。

top_left 和 top_right 的 Detection Score 相对最低，分别为 0.929033 和 0.930278，但它们的 ASR 也处于 9 个位置中的较低水平，分别为 0.9298 和 0.9310。因此，这两个位置并不属于“高 ASR + 低 Detection Score”的典型高隐蔽风险位置，而是表现为攻击效果和检测分数同步降低。

bottom_left 和 bottom_right 的 ASR 分别为 0.9704 和 0.9688，Detection Score 分别为 0.968406 和 0.967315。它们在保持较高攻击成功率的同时，Detection Score 低于 center、middle_right 和 bottom_center，可视为相对更平衡的位置。但由于检测分数仍然高于 0.96，不能将其解释为真正隐蔽，只能说明其相对检测显著性略低。

## 4. 对隐蔽性的判断

按照“高 ASR + 低 Detection Score”作为隐蔽性较强的判断标准，本实验没有出现特别理想的高隐蔽位置。主要原因是本项目使用的触发器为固定 3x3 白色方块，触发器形态简单且目标类别激活明显；同时简化 Detection Score 直接衡量目标类别平均置信度，因此它与 ASR 在数值趋势上天然接近。

因此，本实验更适合得出以下结论：

1. 触发器位置会影响 ASR 和 Detection Score 的大小。
2. 图像中部及偏下区域通常具有更强后门激活效果。
3. 攻击成功率较高的位置往往也更容易被检测。
4. 在当前触发器和检测指标设置下，尚未观察到明显“攻击强且检测困难”的位置。

## 5. 可写入报告的结论

将 ASR 与 Detection Score 结合分析可以发现，不同触发器位置在攻击有效性和检测显著性上呈现同向变化。center、middle_right、bottom_center 等位置具有较高 ASR，同时 Detection Score 也较高，说明这些位置攻击效果强，但后门特征也更明显。top_left 和 top_right 的检测分数相对较低，但其 ASR 也相对较低，未体现出明显的高隐蔽优势。bottom_left 和 bottom_right 在保持较高 ASR 的同时，Detection Score 略低于中心和中右位置，可视为相对更平衡的位置，但仍属于低检测难度范围。总体来看，本实验没有发现典型的“高 ASR + 低检测分数”位置，说明固定白色方块触发器虽然在多数位置均能形成有效后门，但其隐蔽性有限。

## 6. 防御局限性说明

本项目的检测方法是 Neural Cleanse 思想的简化实现，并没有真正执行触发器反向优化和异常类别比较。因此，Detection Score 更适合作为后门激活强度指标，而不是完整防御算法的最终判定结果。后续如果要提高检测可信度，可以进一步实现完整 Neural Cleanse、STRIP 或 Fine-pruning，并比较不同防御方法对触发器位置变化的敏感性。
