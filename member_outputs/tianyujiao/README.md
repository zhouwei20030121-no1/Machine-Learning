# 田玉娇交付目录

田玉娇负责结果合并、消融实验、报告整合和最终提交材料。

## 应提交内容

```text
csv/final_results.csv
csv/poison_rate_ablation.csv
figures/基础图表或最终整合图表
report/课程设计报告.docx
report/课程设计报告.pdf
report/运行说明.txt
notes/合并检查说明.md
notes/最终提交材料说明.md
```

## 合并命令

在 `source_code` 目录下运行：

```bash
python -m analysis.merge_results
```

生成：

```text
source_code/results/csv/final_results.csv
```

## 消融实验命令

```bash
python -m experiments.run_poison_rate_ablation --position bottom_right --rates 0.05 0.10 0.15
```

生成：

```text
source_code/results/csv/poison_rate_ablation.csv
```

最后把结果复制到本目录的 `csv/`，报告和运行说明放到 `report/`。
