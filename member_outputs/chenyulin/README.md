# 陈昱霖交付目录

陈昱霖负责 Neural Cleanse 防御检测与隐蔽性分析。

## 当前完成状态

已完成 9 个触发器位置的 Detection Score 检测，并已整理检测结果、检测模型路径清单和报告分析文字。

已完成文件：

```text
csv/detection_results.csv
models_to_check/model_paths.md
notes/neural_cleanse_principle.md                  # 2.5 防御检测原理
notes/neural_cleanse_detection_difficulty.md       # 3.6 实验设计 + 4.4 检测难度分析
notes/asr_detection_tradeoff_analysis.md           # 4.5 权衡分析 + 5.2 防御局限性
notes/report_sections_2.5_3.6_4.4_4.5.md           # 可直接交给田玉娇整合的章节汇总版
```

## 应提交内容

```text
csv/detection_results.csv
models_to_check/model_paths.md
notes/neural_cleanse_principle.md
notes/neural_cleanse_detection_difficulty.md
notes/asr_detection_tradeoff_analysis.md
notes/report_sections_2.5_3.6_4.4_4.5.md
```

## 对应报告章节

<p align="center">表 1 陈昱霖负责内容与报告章节对应关系</p>

| 报告章节 | 对应文件 |
|---|---|
| 2.5 Neural Cleanse 防御检测原理 | `notes/neural_cleanse_principle.md` |
| 3.6 Neural Cleanse 防御检测实验设计 | `notes/neural_cleanse_detection_difficulty.md`（第 1、2 节） |
| 4.4 不同位置下 Neural Cleanse 检测难度分析 | `notes/neural_cleanse_detection_difficulty.md`（第 3~5 节） |
| 4.5 触发器空间位置与攻击隐蔽性权衡分析 | `notes/asr_detection_tradeoff_analysis.md`（第 1~5 节） |
| 5.2 防御检测方法的不足 | `notes/asr_detection_tradeoff_analysis.md`（第 6 节） |

整合报告时也可以直接使用 `notes/report_sections_2.5_3.6_4.4_4.5.md`，该文件已按报告章节顺序汇总 2.5、3.6、4.4、4.5 的正文内容。

## 检测命令示例

在 `source_code` 目录下运行：

```bash
python -m defense.detection_score --position top_left --model-path results/models/backdoor_top_left.pt
```

9 个位置都检测完后，把 `source_code/results/csv/detection_results.csv` 复制到本目录的 `csv/`。

## 说明文字要包含

- Detection Score 的含义；
- Mask Norm 的含义；
- 哪些位置更容易被检测；
- 哪些位置 ASR 高但 Detection Score 较低，说明更隐蔽；
- 4.4 和 4.5 可直接使用的分析文字。
