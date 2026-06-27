# 李卓尔交付目录

李卓尔负责 5 个触发器位置：

```text
top_left
top_center
top_right
middle_left
center
```

## 应提交内容

```text
csv/asr_acc_results_part1.csv
models/backdoor_top_left.pt
models/backdoor_top_center.pt
models/backdoor_top_right.pt
models/backdoor_middle_left.pt
models/backdoor_center.pt
logs/训练日志
screenshots/运行截图或测试截图
notes/实验现象说明.md
```

## 运行命令

在 `source_code` 目录下运行：

```bash
python -m experiments.run_position --position top_left --part part1
python -m experiments.run_position --position top_center --part part1
python -m experiments.run_position --position top_right --part part1
python -m experiments.run_position --position middle_left --part part1
python -m experiments.run_position --position center --part part1
```

运行结束后，程序会自动写入 `source_code/results/`。如需组内备份，可额外复制到本目录的 `csv/`、`models/`；**课程最终只提交 `source_code/`**，过程性日志和截图只保留在本目录，不要放进 `source_code/`。
