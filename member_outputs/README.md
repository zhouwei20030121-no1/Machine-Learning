# member_outputs 成员交付目录说明

这个目录专门用来放每个成员自己产出的结果文件。代码仍然放在 `source_code/`，成员跑出来的 CSV、模型、截图、日志、说明文字，统一复制到自己名字对应的目录里提交。

## 总原则

1. 代码从 `dev` 分支开自己的分支写。
2. 每个人只把自己负责的结果放进自己的目录。
3. 不要把别人的结果文件放进自己的目录。
4. 文件名尽量保留英文和位置名，方便脚本合并。
5. 提交前先检查 README 中的清单，缺什么补什么。

## 目录结构

```text
member_outputs/
  README.md
    本说明文件，解释每个人应该提交到哪里。

  zhouwei/
    reference_top_left/
      models/backdoor_top_left.pt
        周玮已经完整训练好的 top_left 参考模型，10 轮训练，可供大家参考模型保存格式。
      csv/asr_acc_results_reference_top_left.csv
        周玮已经跑出的 top_left 参考结果，记录 Clean Accuracy 和 ASR。
      notes/
        周玮可放代码说明、实验参数说明、主实验分析草稿。

  lizhuoer/
    csv/
      放李卓尔负责的 5 个位置实验结果表，例如 asr_acc_results_part1.csv。
    models/
      放李卓尔负责的 5 个位置模型，例如 backdoor_top_left.pt。
    logs/
      放训练日志文本。
    screenshots/
      放运行截图、测试截图。
    notes/
      放实验现象说明，例如哪个位置 ASR 高、有没有异常。

  jiasinan/
    csv/
      放贾思楠负责的 4 个位置实验结果表，例如 asr_acc_results_part2.csv。
    models/
      放贾思楠负责的 4 个位置模型。
    logs/
      放训练日志文本。
    screenshots/
      放运行截图、测试截图。
    figures/
      放 ASR 热力图、检测难度热力图、权衡图等最终图表。
    notes/
      放图表说明和理论部分草稿。

  chenyulin/
    csv/
      放 defense/detection_score.py 生成的 detection_results.csv。
    models_to_check/
      可放模型路径清单，不建议重复放所有模型；如果需要临时检测，可放说明。
    notes/
      放 Neural Cleanse 检测难度说明、ASR 与检测难度权衡分析文字。

  tianyujiao/
    csv/
      放 final_results.csv、poison_rate_ablation.csv 等合并结果。
    figures/
      放基础图表或最终整合图表。
    report/
      放最终报告 docx/pdf、运行说明等。
    notes/
      放合并检查说明、格式检查记录、提交材料说明。
```

## 每个人提交到哪里

| 成员 | 主要提交目录 | 必交内容 |
|---|---|---|
| 周玮 | `member_outputs/zhouwei/` | 参考模型、参考 CSV、代码说明、实验参数说明 |
| 李卓尔 | `member_outputs/lizhuoer/` | 5 个位置模型、`asr_acc_results_part1.csv`、日志、截图、现象说明 |
| 贾思楠 | `member_outputs/jiasinan/` | 4 个位置模型、`asr_acc_results_part2.csv`、图表、图表说明 |
| 陈昱霖 | `member_outputs/chenyulin/` | `detection_results.csv`、检测难度说明、权衡分析文字 |
| 田玉娇 | `member_outputs/tianyujiao/` | `final_results.csv`、消融实验结果、最终报告、运行说明 |

## 参考结果

周玮已经放了一个完整训练样例：

```text
member_outputs/zhouwei/reference_top_left/models/backdoor_top_left.pt
member_outputs/zhouwei/reference_top_left/csv/asr_acc_results_reference_top_left.csv
```

参考结果：

```text
Position: top_left
Clean Accuracy: 0.703700
ASR: 0.940600
Epoch: 10
Training Time: 181.63 秒
```

其他成员提交模型和 CSV 时，命名和字段尽量参考这个样例。

## Git 提交流程

所有成员先基于 `dev` 创建自己的分支：

```bash
git switch dev
git pull origin dev
git switch -c feature/你的名字-任务名
```

例如李卓尔：

```bash
git switch dev
git pull origin dev
git switch -c feature/lizhuoer-part1-results
```

提交自己的结果：

```bash
git add member_outputs/你的目录
git commit -m "提交自己的实验结果"
git push -u origin feature/你的名字-任务名
```

然后在 GitHub 上创建 Pull Request，目标分支选择 `dev`。

## 不要提交什么

- 不要提交 `source_code/data/`，CIFAR-10 数据集太大，已经被 `.gitignore` 忽略。
- 不要提交临时 Word 文件，例如 `~$xxx.docx`。
- 不要把重复 CSV 或失败实验模型混在最终结果里。
- 如果某个位置重跑了，保留最终正确版本，把旧版本移动到 notes 说明或删除。

## 实验结果双目录规则

实验结果需要同时保留在两个位置：

1. `source_code/results/`：程序运行目录，训练、检测、合并脚本默认从这里读写文件。
2. `member_outputs/个人目录/`：成员提交目录，用来归档每个人自己的产出，方便组长检查和 GitHub 提交。

也就是说，大家运行代码后，先让程序自动输出到 `source_code/results/`，然后再把自己负责的结果复制到 `member_outputs/自己的目录/`。

### 为什么要放两份

`source_code/results/` 的作用是给代码继续运行用：

```text
source_code/results/csv/       # 脚本默认读取和写入 CSV
source_code/results/models/    # 训练脚本默认保存模型
source_code/results/logs/      # 训练日志
source_code/figures/           # 绘图脚本默认输出图表
```

`member_outputs/` 的作用是给人检查和提交用：

```text
member_outputs/lizhuoer/       # 李卓尔自己的实验结果
member_outputs/jiasinan/       # 贾思楠自己的实验结果和图表
member_outputs/chenyulin/      # 陈昱霖的检测结果和分析文字
member_outputs/tianyujiao/     # 田玉娇的合并结果和报告
member_outputs/zhouwei/        # 周玮的参考模型和说明
```

### 示例：李卓尔跑完实验后

程序会自动生成：

```text
source_code/results/csv/asr_acc_results_part1.csv
source_code/results/models/backdoor_top_left.pt
source_code/results/models/backdoor_top_center.pt
source_code/results/models/backdoor_top_right.pt
source_code/results/models/backdoor_middle_left.pt
source_code/results/models/backdoor_center.pt
```

然后李卓尔还需要复制一份到：

```text
member_outputs/lizhuoer/csv/asr_acc_results_part1.csv
member_outputs/lizhuoer/models/backdoor_top_left.pt
member_outputs/lizhuoer/models/backdoor_top_center.pt
member_outputs/lizhuoer/models/backdoor_top_right.pt
member_outputs/lizhuoer/models/backdoor_middle_left.pt
member_outputs/lizhuoer/models/backdoor_center.pt
```

### 示例：贾思楠跑完实验后

程序会自动生成：

```text
source_code/results/csv/asr_acc_results_part2.csv
source_code/results/models/backdoor_middle_right.pt
source_code/results/models/backdoor_bottom_left.pt
source_code/results/models/backdoor_bottom_center.pt
source_code/results/models/backdoor_bottom_right.pt
```

然后贾思楠还需要复制一份到：

```text
member_outputs/jiasinan/csv/asr_acc_results_part2.csv
member_outputs/jiasinan/models/backdoor_middle_right.pt
member_outputs/jiasinan/models/backdoor_bottom_left.pt
member_outputs/jiasinan/models/backdoor_bottom_center.pt
member_outputs/jiasinan/models/backdoor_bottom_right.pt
```

### 注意

`source_code/results/` 是运行用目录，里面的模型和 CSV 可能会被反复覆盖；`member_outputs/个人目录/` 是提交用目录，大家最终检查时主要看这里。
