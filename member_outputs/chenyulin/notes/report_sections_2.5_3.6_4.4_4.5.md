# 陈昱霖负责报告章节汇总

本文档汇总陈昱霖负责的报告正文内容，对应第 2.5、3.6、4.4、4.5 节，可交给田玉娇直接整合进课程设计报告。表注已按“表注置于表格上方并居中”的格式处理。

## 2.5 Neural Cleanse 防御检测原理

后门攻击的典型特点是：模型在干净样本上保持较高分类准确率，但当输入样本中出现攻击者预设的触发器时，模型会被定向误分类到目标类别。因此，仅观察模型在正常测试集上的准确率，通常无法判断模型是否被植入后门。Neural Cleanse 的核心思想是在不知道触发器具体形状和位置的情况下，反向搜索可能存在的触发器，并据此判断模型是否存在异常目标类别。

Neural Cleanse 将后门检测转化为触发器反向优化问题。对于每一个候选类别，方法尝试寻找一个尽可能小的掩码和触发器图案，使得大量干净样本叠加该扰动后都被模型预测为该候选类别。其输入变换可以表示为：

```text
x' = (1 - m) * x + m * Δ
```

其中，`x` 表示原始输入图像，`x'` 表示叠加触发器后的图像，`m` 表示触发器掩码，`Δ` 表示触发器图案。优化目标是在保证样本被预测为指定类别的同时，使掩码 `m` 尽可能小。若某个类别是后门攻击的目标类别，模型已经学习到“小触发器到目标类别”的异常关联，因此只需要较小的触发器掩码就能让大量样本被预测为该类别。相反，正常类别通常需要更大范围的扰动才能产生类似效果。

因此，Neural Cleanse 会比较不同类别反向优化得到的掩码大小，并通过异常检测方法判断是否存在明显偏小的掩码。如果某一类别对应的掩码范数显著低于其他类别，则说明该类别可能是后门目标类别，模型存在被植入后门的风险。从检测难度角度看，触发器越小、越稳定、越容易被反向恢复，其检测难度越低；如果触发器特征不明显，或者不同类别之间的掩码差异不大，则检测难度相对更高。

受课程设计时间和算力限制，本项目没有实现完整 Neural Cleanse 的逐类别反向优化流程，而是借鉴其“从触发器显著性判断后门风险”的思想，设计简化版 Detection Score 指标。该指标衡量添加指定位置触发器后，模型预测为目标类别的平均置信度。Detection Score 越高，表示该位置触发器对目标类别的激活越明显，后门特征越容易被检测；Detection Score 越低，则说明触发器激活目标类别的平均置信度相对较弱，检测难度相对更高。

## 3.6 Neural Cleanse 防御检测实验设计

本实验的防御检测对象为 9 个不同触发器位置训练得到的后门模型。模型分别对应 `top_left`、`top_center`、`top_right`、`middle_left`、`center`、`middle_right`、`bottom_left`、`bottom_center`、`bottom_right` 九个位置。检测阶段固定目标类别为 0，触发器仍采用 3x3 白色方块，与前序后门攻击实验保持一致，保证检测结果能够与 Clean Accuracy 和 ASR 结果进行对比分析。

完整 Neural Cleanse 需要对每个类别分别进行触发器反向优化，计算量较大。考虑到课程设计的时间和硬件条件，本项目采用简化检测指标 Detection Score 作为代理指标。具体做法是：对 CIFAR-10 测试集样本添加指定位置触发器，将触发器样本输入对应位置训练得到的后门模型，计算模型输出为目标类别 0 的 softmax 概率，并对全部测试样本求平均。其计算形式如下：

```text
Detection Score = mean(P(y = target_label | x_triggered))
```

其中，`x_triggered` 表示添加触发器后的测试样本，`target_label` 为目标类别 0。该指标反映触发器对目标类别的平均激活强度。Detection Score 越高，说明模型越稳定地将含触发器样本识别为目标类别，后门特征越明显，检测难度越低；Detection Score 越低，说明该位置触发器对目标类别的激活不够强，检测难度相对更高。

除 Detection Score 外，本项目还记录 Mask Norm，用于描述触发器掩码大小。由于所有位置均使用相同的 3x3 触发器，CIFAR-10 图像大小为 32x32，因此 Mask Norm 固定为：

```text
Mask Norm = 3 * 3 / (32 * 32) = 0.008789
```

由于触发器大小不随位置变化，Mask Norm 在 9 个位置中保持一致，本实验主要通过 Detection Score 比较不同位置的检测显著性。检测难度等级按以下规则划分。

<p align="center">表 1 Detection Difficulty 判定规则</p>

| Detection Score 范围 | Detection Difficulty |
|---:|---|
| score >= 0.80 | Low Detection Difficulty |
| 0.50 <= score < 0.80 | Medium Detection Difficulty |
| score < 0.50 | High Detection Difficulty |

需要说明的是，`Low Detection Difficulty` 表示检测难度低，即更容易被检测，不表示攻击风险低。本实验通过 `source_code/defense/detection_score.py` 逐个读取 9 个后门模型并输出 `detection_results.csv`，供后续结果合并、检测热力图绘制和隐蔽性权衡分析使用。

## 4.4 不同触发器位置下 Neural Cleanse 检测难度分析

本节基于简化 Detection Score 指标，分析不同触发器位置下后门特征的检测显著性。检测结果如表 2 所示。

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

从整体结果看，9 个触发器位置的 Detection Score 均高于 0.92，全部被划分为 `Low Detection Difficulty`。这说明在本实验设定下，固定 3x3 白色方块触发器在不同空间位置上都能明显激活目标类别，后门特征整体较为显著，简化检测指标能够较容易地捕捉到触发器引起的异常目标类别响应。

虽然 9 个位置的检测难度等级相同，但 Detection Score 仍存在一定差异。按 Detection Score 从高到低排序，分数最高的几个位置为 `center`、`middle_right`、`bottom_center` 和 `middle_left`，其检测分数均接近或超过 0.974。其中 `center` 的 Detection Score 为 0.980641，`middle_right` 为 0.980572，说明图像中部及偏中右区域的触发器对目标类别激活最强，后门特征也最容易被检测。

相对而言，`top_left` 和 `top_right` 的 Detection Score 最低，分别为 0.929033 和 0.930278。这表明顶部角落位置的触发器相对不如中心和中右位置显著。但这两个分数仍明显高于 0.80 的低检测难度阈值，因此不能认为顶部角落位置具有高检测难度，只能说明它们在 9 个位置中相对不那么显著。

综合来看，触发器空间位置会影响 Detection Score 的大小：图像中部及偏下区域通常检测分数更高，顶部角落位置检测分数相对较低。但由于所有位置均属于低检测难度，本实验尚未观察到从“容易检测”到“难以检测”的显著等级差异。

## 4.5 触发器空间位置与攻击隐蔽性权衡分析

为进一步分析触发器位置对攻击有效性和隐蔽性的影响，本节将前序实验得到的 ASR 与本实验得到的 Detection Score 进行联合分析。若某个位置同时具有较高 ASR 和较低 Detection Score，可以认为该位置具有较高隐蔽风险；若 ASR 高但 Detection Score 也高，则说明攻击有效，但后门特征也更容易被检测。联合结果如表 3 所示。

<p align="center">表 3 ASR 与 Detection Score 联合分析结果</p>

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

从表 3 可以看出，ASR 与 Detection Score 呈现高度一致的变化趋势。ASR 较高的位置通常也具有较高的 Detection Score。例如，`center`、`middle_right`、`bottom_center` 和 `middle_left` 的 ASR 均高于 0.974，同时 Detection Score 也都高于 0.973。这说明这些位置的触发器攻击成功率较高，但后门特征也更明显，更容易被简化检测指标捕捉到。

`top_left` 和 `top_right` 的 Detection Score 相对最低，分别为 0.929033 和 0.930278，但其 ASR 也处于 9 个位置中的较低水平，分别为 0.9298 和 0.9310。因此，这两个位置并不属于“高 ASR + 低 Detection Score”的典型高隐蔽风险位置，而是表现为攻击成功率和检测显著性同步降低。

`bottom_left` 和 `bottom_right` 的 ASR 分别为 0.9704 和 0.9688，Detection Score 分别为 0.968406 和 0.967315。二者在保持较高攻击成功率的同时，Detection Score 低于 `center`、`middle_right` 和 `bottom_center`，可以视为相对更平衡的位置。但由于检测分数仍高于 0.96，仍不能将其解释为真正难以检测的位置，只能说明其相对检测显著性略低。

总体来看，本实验未发现典型的“高 ASR + 低 Detection Score”位置。这说明固定 3x3 白色方块触发器虽然在多数位置都能形成有效后门，但其隐蔽性有限。触发器越能稳定激活目标类别，攻击成功率越高，同时也越容易被检测指标捕捉到。因此，在当前实验设置下，触发器位置对攻击有效性和检测显著性均有影响，但没有形成明显的高隐蔽优势位置。

需要注意的是，本项目采用的是 Neural Cleanse 思想的简化检测实现，并未执行完整的触发器反向优化和异常类别比较。因此，Detection Score 更适合作为后门激活强度指标，而不能完全等同于完整防御算法的最终检测结论。后续若要提高防御评估的可信度，可以进一步实现完整 Neural Cleanse、STRIP 或 Fine-pruning 等方法，并比较不同防御方法对触发器空间位置变化的敏感性。

