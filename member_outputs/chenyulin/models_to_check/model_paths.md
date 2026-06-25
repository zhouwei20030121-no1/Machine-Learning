# 检测模型路径清单

本次防御检测共检查 9 个后门模型。模型来源于李卓尔的 `member_outputs/lizhuoer/models/`（part1 五个位置）和贾思楠的 `member_outputs/jiasinan/models/`（part2 四个位置）。检测时将这些模型复制到运行目录 `source_code/results/models/`（该目录被 `.gitignore` 忽略，仅作运行使用），再用项目默认检测脚本 `python -m defense.detection_score` 逐个计算 Detection Score。

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
