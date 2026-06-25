# 陈昱霖交付目录

陈昱霖负责 Neural Cleanse 防御检测与隐蔽性分析。

## 当前完成状态

已完成 9 个触发器位置的 Detection Score 检测，并已提交检测结果和分析文字。

已完成文件：

```text
csv/detection_results.csv
models_to_check/model_paths.md
notes/neural_cleanse_detection_difficulty.md
notes/asr_detection_tradeoff_analysis.md
```

## 应提交内容

```text
csv/detection_results.csv
notes/neural_cleanse_detection_difficulty.md
notes/asr_detection_tradeoff_analysis.md
```

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
