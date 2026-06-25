# 检测模型路径清单

本次防御检测共检查 9 个后门模型。运行检测时，已将模型复制到 `source_code/results/models/`，并使用项目默认检测脚本 `python -m defense.detection_score` 逐个计算 Detection Score。

<p align="center">表 1 检测模型路径</p>

| Position | Model Path |
|---|---|
| top_left | `source_code/results/models/backdoor_top_left.pt` |
| top_center | `source_code/results/models/backdoor_top_center.pt` |
| top_right | `source_code/results/models/backdoor_top_right.pt` |
| middle_left | `source_code/results/models/backdoor_middle_left.pt` |
| center | `source_code/results/models/backdoor_center.pt` |
| middle_right | `source_code/results/models/backdoor_middle_right.pt` |
| bottom_left | `source_code/results/models/backdoor_bottom_left.pt` |
| bottom_center | `source_code/results/models/backdoor_bottom_center.pt` |
| bottom_right | `source_code/results/models/backdoor_bottom_right.pt` |

检测结果已归档到：

```text
member_outputs/chenyulin/csv/detection_results.csv
```
