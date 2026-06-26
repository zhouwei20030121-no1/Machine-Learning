# 田玉娇交付说明

负责人：田玉娇  
交付日期：2026-06-26  
项目：基于 CIFAR-10 的后门攻击触发器位置空间敏感性分析

---

## 一、本人负责内容

| 任务 | 状态 |
|---|---|
| 合并 9 个位置攻击结果与防御检测结果 | 已完成 |
| 投毒比例消融实验 | 已完成 |
| 基础图表生成 | 已完成 |
| 运行说明与提交清单 | 已完成 |
| 课程设计报告整合（docx / pdf） | 待完成 |

---

## 二、目录结构

```text
member_outputs/tianyujiao/
├── README.md                          # 本文件，交付总说明
├── csv/
│   ├── final_results.csv              # 9 位置合并最终结果
│   └── poison_rate_ablation.csv       # 投毒比例消融结果
├── figures/
│   ├── asr_heatmap_basic.png          # ASR 九宫格热力图
│   ├── detection_heatmap_basic.png    # 检测分数九宫格热力图
│   ├── acc_asr_bar_basic.png          # Clean Accuracy / ASR 柱状图
│   ├── asr_detection_tradeoff.png     # ASR 与检测分数权衡散点图
│   ├── trigger_samples_grid.png       # 触发器位置样例九宫格
│   └── poison_rate_ablation_bar.png   # 投毒比例消融柱状图
├── notes/
│   ├── 合并检查说明.md                # 合并与实验检查记录
│   └── 最终提交材料说明.md            # 最终提交清单
└── report/
    └── 运行说明.txt                   # 项目运行与复现说明
```

---

## 三、数据文件说明

### 1. `csv/final_results.csv`

合并李卓尔 part1（5 个位置）、贾思楠 part2（4 个位置）与陈昱霖检测结果后生成。

| 字段 | 说明 |
|---|---|
| Position | 触发器位置 |
| Clean Accuracy | 干净样本分类准确率 |
| ASR | 攻击成功率 |
| Detection Score | Neural Cleanse 检测分数 |
| Mask Norm | 触发器掩码范数 |
| Detection Difficulty | 检测难度等级 |
| Tradeoff Type | ASR 与检测分数权衡类型 |

**数据来源：**

- `member_outputs/lizhuoer/csv/asr_acc_results_part1.csv`
- `member_outputs/jiasinan/csv/asr_acc_results_part2.csv`
- `member_outputs/chenyulin/csv/detection_results.csv`

### 2. `csv/poison_rate_ablation.csv`

固定位置 `bottom_right`，测试投毒比例 0.05、0.10、0.15 对 Clean Accuracy 和 ASR 的影响。其余参数与主实验一致（10 epoch、目标类别 0、随机种子 2026）。

| Poison Rate | Clean Accuracy | ASR |
|---:|---:|---:|
| 0.05 | 0.7736 | 0.9443 |
| 0.10 | 0.7515 | 0.9688 |
| 0.15 | 0.7612 | 0.9703 |

---

## 四、图表说明

| 文件名 | 用途建议 |
|---|---|
| `asr_heatmap_basic.png` | 报告主实验：各位置 ASR 空间分布 |
| `detection_heatmap_basic.png` | 报告防御分析：各位置检测难度分布 |
| `acc_asr_bar_basic.png` | 报告对比：主任务精度与攻击效果 |
| `asr_detection_tradeoff.png` | 辅助说明 ASR 与检测分数关系（点较集中，建议配合热力图使用） |
| `trigger_samples_grid.png` | 方法说明：3×3 白色触发器在 9 个位置的示意 |
| `poison_rate_ablation_bar.png` | 消融实验：投毒比例影响 |

---

## 五、主要结论（实验部分）

1. **攻击有效性**：9 个位置 ASR 均高于 0.92，后门攻击均有效。
2. **位置敏感性**：ASR 最高为 `center`（0.9817）和 `middle_right`（0.9820）；Clean Accuracy 最低为 `top_right`（0.7122）。
3. **防御检测**：各位置 Detection Score 均较高（>0.92），`Tradeoff Type` 均为「高 ASR + 高检测分数」，在本实验设置下较易被检出。
4. **消融实验**：投毒比例从 0.05 升至 0.15，ASR 从 0.9443 增至 0.9703；Clean Accuracy 在 0.75～0.77 间波动，未明显崩溃。

更详细的检查记录见 `notes/合并检查说明.md`。

---

## 六、复现命令

在 `source_code` 目录下执行：

```bash
# 1. 合并结果（需先将三份输入 CSV 放到 source_code/results/csv/）
python -m analysis.merge_results

# 2. 消融实验
python -m experiments.run_poison_rate_ablation --position bottom_right --rates 0.05 0.10 0.15

# 3. 生成基础图表
python -m analysis.plot_results
python -m analysis.visualize_trigger_samples
```

程序默认输出到 `source_code/results/csv/` 和 `source_code/figures/`，提交用副本在本目录 `csv/` 与 `figures/`。

---

## 七、交付对象与用途

| 接收人 | 可用材料 | 用途 |
|---|---|---|
| 贾思楠 | `final_results.csv`、基础图表 | 画最终图、插入报告 |
| 周玮 | `final_results.csv`、消融结果、图表 | 主实验分析、报告统稿 |
| 全组 | 本目录全部实验产出 | 组内检查与最终提交 |

---

## 八、待补充

- `report/课程设计报告.docx`
- `report/课程设计报告.pdf`

运行说明见 `report/运行说明.txt`，提交清单见 `notes/最终提交材料说明.md`。
