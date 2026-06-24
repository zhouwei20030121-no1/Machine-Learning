# 贾思楠交付目录

贾思楠负责 4 个触发器位置和最终图表：

```text
middle_right
bottom_left
bottom_center
bottom_right
```

## 应提交内容

```text
csv/asr_acc_results_part2.csv
models/backdoor_middle_right.pt
models/backdoor_bottom_left.pt
models/backdoor_bottom_center.pt
models/backdoor_bottom_right.pt
figures/asr_heatmap.png
figures/detection_heatmap.png
figures/acc_asr_bar.png
figures/asr_detection_tradeoff.png
figures/poison_rate_ablation.png
logs/训练日志
screenshots/运行截图或测试截图
notes/图表说明.md
```

## 运行命令

在 `source_code` 目录下运行：

```bash
python -m experiments.run_position --position middle_right --part part2
python -m experiments.run_position --position bottom_left --part part2
python -m experiments.run_position --position bottom_center --part part2
python -m experiments.run_position --position bottom_right --part part2
```

运行结束后，把 `source_code/results/csv/asr_acc_results_part2.csv` 复制到本目录的 `csv/`，把对应模型复制到本目录的 `models/`。
