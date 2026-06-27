# 田玉娇交付目录

田玉娇负责结果合并、投毒比例消融实验、图表生成与报告整合。

## 应提交内容

```text
csv/final_results.csv
csv/poison_rate_ablation.csv
figures/asr_heatmap_basic.png
figures/detection_heatmap_basic.png
figures/acc_asr_bar_basic.png
figures/asr_detection_tradeoff.png
figures/trigger_samples_grid.png
figures/poison_rate_ablation_bar.png
notes/合并检查说明.md
notes/最终提交材料说明.md
```

## 运行命令

在 `source_code` 目录下运行：

```bash
python -m analysis.merge_results
python -m experiments.run_poison_rate_ablation --position bottom_right --rates 0.05 0.10 0.15
python -m analysis.plot_results
python -m analysis.visualize_trigger_samples
```

合并前需先将 part1、part2、detection 三份 CSV 放入 `source_code/results/csv/`。

运行结束后，程序会自动写入 `source_code/results/` 和 `source_code/figures/`。如需组内备份，可额外复制到本目录；**课程最终只提交 `source_code/`**，过程性日志和截图不要放进 `source_code/`。

## 报告对应章节（机器学习报告 3.0）

| 章节 | 内容 |
|---|---|
| 2.2.4 | 投毒比例消融问题定义 |
| 3.7.1 / 3.7.2 | 投毒比例消融实验设计（含图 3-7-1 流程图） |
| 4.6.1 / 4.6.2 | 投毒比例消融实验分析（图 4-6-1 使用 `poison_rate_ablation_bar.png`） |
| 5.2.4 | 消融实验模块（`run_poison_rate_ablation.py`、`merge_results.py` 等） |

项目整体运行说明见仓库根目录 `运行说明.txt`。
