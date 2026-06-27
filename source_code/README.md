# source_code 运行说明

本目录是课程设计的代码主目录。代码已经按照任务分工搭好框架，其他同学只需要按自己的分工运行对应命令，并把生成的 CSV、模型路径、日志和说明交给对应负责人。

## 1. 实验目标

在 CIFAR-10 图像分类任务上实现 BadNets 后门攻击，并比较 3x3 九个触发器位置对以下指标的影响：

- Clean Accuracy：干净测试集准确率；
- ASR：Attack Success Rate，攻击成功率；
- Detection Score：简化 Neural Cleanse 检测分数；
- Mask Norm：触发器掩码大小的简化度量；
- Detection Difficulty：检测难度等级；
- Tradeoff Type：ASR 与检测分数的权衡类型。

## 2. 统一参数

| 参数 | 默认值 | 说明 |
|---|---:|---|
| 数据集 | CIFAR-10 | 第一次运行自动下载 |
| 模型 | Simple CNN | `models/cnn_model.py` |
| 触发器 | 3x3 白色方块 | `utils/trigger_utils.py` |
| 目标类别 | 0 | 所有投毒样本标签改为 0 |
| 投毒比例 | 0.10 | 主实验固定 |
| 训练轮数 | 10 | 可按时间改为 20，但 9 个位置必须一致 |
| Batch Size | 128 | 主实验固定 |
| 学习率 | 0.001 | Adam |
| 随机种子 | 2026 | 保证可复现 |

重要要求：主实验中 9 个位置只能改 `--position`，不要随便改 `--poison-rate`、`--epochs`、`--target-label`。如果确实要改，必须 9 个位置全部使用同一设置。

## 3. 触发器位置名称

代码中固定使用以下 9 个位置名称：

```text
top_left       top_center       top_right
middle_left    center           middle_right
bottom_left    bottom_center    bottom_right
```

运行命令里的 `--position` 必须写成上面这些英文名称。

## 4. 完整目录结构

```text
source_code/
  README.md
  requirements.txt

  models/
    __init__.py
    cnn_model.py
      SimpleCNN 模型。输入为 CIFAR-10 的 3x32x32 图像，输出 10 类分类结果。

  utils/
    __init__.py
    config.py
      统一保存路径、随机种子、训练参数、9 个触发器位置。

    trigger_utils.py
      add_trigger(image, position)：给单张图加触发器。
      add_trigger_batch(images, position)：给一批图加触发器。

    dataset_poison.py
      PoisonedDataset：包装 CIFAR-10 训练集，按投毒比例添加触发器并修改标签。
      choose_poison_indices：固定随机种子选择投毒样本。

    train_utils.py
      数据集加载、DataLoader、模型构建、训练一轮、准确率评估、保存 checkpoint。

  experiments/
    __init__.py
    train_backdoor.py
      训练某一个触发器位置的后门模型，输出模型权重。

    evaluate_clean_acc.py
      读取模型，在干净测试集上计算 Clean Accuracy。

    evaluate_asr.py
      读取模型，在带触发器测试集上计算 ASR。

    run_position.py
      最常用入口。完成：训练模型 -> 测 Clean Accuracy -> 测 ASR -> 写 CSV。

    run_poison_rate_ablation.py
      投毒比例消融实验入口，默认测试 0.05、0.10、0.15。

  defense/
    __init__.py
    detection_score.py
      简化 Neural Cleanse 检测。读取模型后，计算触发器样本被预测成目标类别的平均置信度。

  analysis/
    __init__.py
    merge_results.py
      合并 asr_acc_results_part1.csv、asr_acc_results_part2.csv、detection_results.csv。

    plot_results.py
      根据 final_results.csv 生成基础图表。

    visualize_trigger_samples.py
      生成 9 个触发器位置的样本九宫格。

  results/
    csv/
      asr_acc_results_part1.csv       李卓尔输出
      asr_acc_results_part2.csv       贾思楠输出
      detection_results.csv           陈昱霖输出
      final_results.csv               田玉娇合并输出
      poison_rate_ablation.csv        田玉娇消融实验输出

    models/
      backdoor_<position>.pt          每个位置的后门模型

    logs/
      可存放训练日志

    figures/
      asr_heatmap_basic.png
      detection_heatmap_basic.png
      acc_asr_bar_basic.png
      asr_detection_tradeoff.png
      poison_rate_ablation_bar.png
      trigger_samples_grid.png

  test_data/
    screenshots/
      可存放运行截图和测试截图
```

## 5. 环境安装

建议使用 Python 3.10 或 3.11。

进入代码目录：

```bash
cd source_code
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果 PyTorch 安装较慢或失败，可以到 PyTorch 官网选择适合自己电脑 CUDA/CPU 的安装命令。其他依赖只有 `numpy`、`pandas`、`matplotlib`。

## 6. 周玮交付给大家的运行方式

最重要的统一入口是：

```bash
python -m experiments.run_position --position 位置名称 --part part1或part2
```

这个命令会自动完成：

1. 加载 CIFAR-10；
2. 按指定位置添加 BadNets 触发器；
3. 训练后门模型；
4. 保存模型到 `results/models/backdoor_<position>.pt`；
5. 测 Clean Accuracy；
6. 测 ASR；
7. 把结果写入 `results/csv/asr_acc_results_part1.csv` 或 `results/csv/asr_acc_results_part2.csv`。

## 7. 李卓尔运行命令

李卓尔负责 5 个位置，全部使用 `--part part1`：

```bash
python -m experiments.run_position --position top_left --part part1
python -m experiments.run_position --position top_center --part part1
python -m experiments.run_position --position top_right --part part1
python -m experiments.run_position --position middle_left --part part1
python -m experiments.run_position --position center --part part1
```

李卓尔需要提交：

| 文件/内容 | 交给谁 | 用途 |
|---|---|---|
| `results/csv/asr_acc_results_part1.csv` | 田玉娇 | 合并最终结果 |
| 5 个模型路径 | 陈昱霖 | 做防御检测 |
| 训练日志、截图 | 田玉娇 | 附录或测试数据 |
| 实验现象说明 | 周玮 | 写 4.2、4.3 |

实验现象说明建议写：

- 哪个位置 ASR 最高；
- 哪个位置 ASR 最低；
- Clean Accuracy 有没有明显下降；
- 训练是否正常收敛；
- 有没有异常值或重跑情况。

## 8. 贾思楠运行命令

贾思楠负责 4 个位置，全部使用 `--part part2`：

```bash
python -m experiments.run_position --position middle_right --part part2
python -m experiments.run_position --position bottom_left --part part2
python -m experiments.run_position --position bottom_center --part part2
python -m experiments.run_position --position bottom_right --part part2
```

贾思楠需要提交：

| 文件/内容 | 交给谁 | 用途 |
|---|---|---|
| `results/csv/asr_acc_results_part2.csv` | 田玉娇 | 合并最终结果 |
| 4 个模型路径 | 陈昱霖 | 做防御检测 |
| 最终图表 | 田玉娇 | 插入最终报告 |
| 图表说明 | 周玮、陈昱霖、田玉娇 | 第 4 章分析 |

## 9. 单独训练或单独测试

通常用 `run_position.py` 就够了。如果只想单独执行某一步，可以用下面的命令。

只训练模型：

```bash
python -m experiments.train_backdoor --position top_left
```

只测试 Clean Accuracy：

```bash
python -m experiments.evaluate_clean_acc --model-path results/models/backdoor_top_left.pt
```

只测试 ASR：

```bash
python -m experiments.evaluate_asr --position top_left --model-path results/models/backdoor_top_left.pt
```

## 10. 陈昱霖防御检测命令

陈昱霖拿到 9 个模型后，对每个位置运行一次：

```bash
python -m defense.detection_score --position top_left --model-path results/models/backdoor_top_left.pt
python -m defense.detection_score --position top_center --model-path results/models/backdoor_top_center.pt
python -m defense.detection_score --position top_right --model-path results/models/backdoor_top_right.pt
python -m defense.detection_score --position middle_left --model-path results/models/backdoor_middle_left.pt
python -m defense.detection_score --position center --model-path results/models/backdoor_center.pt
python -m defense.detection_score --position middle_right --model-path results/models/backdoor_middle_right.pt
python -m defense.detection_score --position bottom_left --model-path results/models/backdoor_bottom_left.pt
python -m defense.detection_score --position bottom_center --model-path results/models/backdoor_bottom_center.pt
python -m defense.detection_score --position bottom_right --model-path results/models/backdoor_bottom_right.pt
```

输出文件：

```text
results/csv/detection_results.csv
```

陈昱霖需要提交：

| 文件/内容 | 交给谁 | 用途 |
|---|---|---|
| `results/csv/detection_results.csv` | 田玉娇 | 合并最终结果 |
| Neural Cleanse 检测难度说明 | 贾思楠 | 画检测热力图和图注 |
| ASR 与检测难度权衡分析 | 田玉娇、周玮 | 写 4.5 |

## 11. 田玉娇合并结果

当下面 3 个文件都齐了以后：

```text
results/csv/asr_acc_results_part1.csv
results/csv/asr_acc_results_part2.csv
results/csv/detection_results.csv
```

运行：

```bash
python -m analysis.merge_results
```

输出：

```text
results/csv/final_results.csv
```

`final_results.csv` 包含：

```text
Position
Clean Accuracy
ASR
Detection Score
Mask Norm
Detection Difficulty
Tradeoff Type
```

其中 `Tradeoff Type` 的含义：

| 类型 | 含义 |
|---|---|
| 高 ASR + 高检测分数 | 攻击有效，但容易被发现 |
| 高 ASR + 低检测分数 | 攻击有效且更隐蔽 |
| 低 ASR + 高检测分数 | 攻击效果一般，但特征明显 |
| 低 ASR + 低检测分数 | 攻击效果弱，检测也不明显 |

## 12. 生成基础图表

合并出 `final_results.csv` 后运行：

```bash
python -m analysis.plot_results
```

输出到 `results/figures/`：

```text
asr_heatmap_basic.png
detection_heatmap_basic.png
acc_asr_bar_basic.png
asr_detection_tradeoff.png
```

生成触发器样本九宫格：

```bash
python -m analysis.visualize_trigger_samples
```

输出：

```text
results/figures/trigger_samples_grid.png
```

## 13. 投毒比例消融实验

默认固定 `bottom_right`，测试 0.05、0.10、0.15：

```bash
python -m experiments.run_poison_rate_ablation --position bottom_right --rates 0.05 0.10 0.15
```

输出：

```text
results/csv/poison_rate_ablation.csv
```

这部分给田玉娇写 3.7 和 4.6 使用，也交给贾思楠画投毒比例消融图。

## 14. 输出文件检查清单

主实验跑完后应该至少有：

```text
results/csv/asr_acc_results_part1.csv
results/csv/asr_acc_results_part2.csv
results/csv/detection_results.csv
results/csv/final_results.csv
results/models/backdoor_top_left.pt
results/models/backdoor_top_center.pt
results/models/backdoor_top_right.pt
results/models/backdoor_middle_left.pt
results/models/backdoor_center.pt
results/models/backdoor_middle_right.pt
results/models/backdoor_bottom_left.pt
results/models/backdoor_bottom_center.pt
results/models/backdoor_bottom_right.pt
```

图表至少有：

```text
results/figures/asr_heatmap_basic.png
results/figures/detection_heatmap_basic.png
results/figures/acc_asr_bar_basic.png
results/figures/asr_detection_tradeoff.png
results/figures/poison_rate_ablation_bar.png
results/figures/trigger_samples_grid.png
```

## 15. 常见问题

### 1. 运行命令提示找不到模块

确认当前目录是 `source_code`，不要在项目根目录直接运行：

```bash
cd source_code
python -m experiments.run_position --position top_left --part part1
```

### 2. CIFAR-10 下载失败

第一次运行会自动下载数据。如果网络不稳定，可以多试一次，或者手动把 CIFAR-10 放到：

```text
source_code/data/
```

### 3. 结果 CSV 里出现重复位置

说明同一个位置重复跑并追加写入了 CSV。可以手动删除 CSV 中重复行，或者删掉该 CSV 后重新跑对应负责人的全部位置。

### 4. 显存不够或运行太慢

可以临时减小 batch size：

```bash
python -m experiments.run_position --position top_left --part part1 --batch-size 64
```

但同一批主实验最好保持 batch size 一致。

### 5. 不同位置结果差异很奇怪

先检查是否只改了 `--position`。如果有人改了 `--epochs`、`--poison-rate` 或 `--target-label`，这个位置需要按统一参数重跑。

## 16. 周玮需要交给其他人的内容

| 交付内容 | 文件/说明 | 交给谁 |
|---|---|---|
| 代码框架 | 本 `source_code/` 目录 | 全体成员 |
| 运行命令 | 本 README 第 6-13 节 | 李卓尔、贾思楠、陈昱霖、田玉娇 |
| 模型保存规则 | `results/models/backdoor_<position>.pt` | 陈昱霖 |
| 触发器函数 | `utils/trigger_utils.py` | 田玉娇 |
| 实验参数说明 | `utils/config.py` 和本 README 第 2 节 | 贾思楠 |
| 实验部分报告依据 | 训练、评估、结果 CSV 和图表 | 田玉娇 |

## 17. 实验结果双目录提交规则

实验脚本默认把结果写到 `source_code/results/`，这个目录是给程序继续读取用的；成员最终提交时，还需要把自己负责的结果复制到项目根目录下的 `member_outputs/个人目录/`。

### 程序运行目录

```text
source_code/results/csv/       # run_position、detection_score、merge_results 默认读写 CSV
source_code/results/models/    # train_backdoor 默认保存模型
source_code/results/logs/      # 可放训练日志
source_code/results/figures/   # plot_results、visualize_trigger_samples 默认输出最终图表
```

### 成员提交目录

```text
member_outputs/lizhuoer/       # 李卓尔提交 5 个位置实验结果
member_outputs/jiasinan/       # 贾思楠提交 4 个位置实验结果和图表
member_outputs/chenyulin/      # 陈昱霖提交检测结果和分析文字
member_outputs/tianyujiao/     # 田玉娇提交合并结果、消融结果、报告
member_outputs/zhouwei/        # 周玮提交参考模型、代码说明、参数说明
```

### 复制示例

李卓尔跑完后，把程序输出复制到自己的目录：

```powershell
Copy-Item source_code\results\csv\asr_acc_results_part1.csv member_outputs\lizhuoer\csv\ -Force
Copy-Item source_code\results\models\backdoor_top_left.pt member_outputs\lizhuoer\models\ -Force
Copy-Item source_code\results\models\backdoor_top_center.pt member_outputs\lizhuoer\models\ -Force
Copy-Item source_code\results\models\backdoor_top_right.pt member_outputs\lizhuoer\models\ -Force
Copy-Item source_code\results\models\backdoor_middle_left.pt member_outputs\lizhuoer\models\ -Force
Copy-Item source_code\results\models\backdoor_center.pt member_outputs\lizhuoer\models\ -Force
```

贾思楠跑完后：

```powershell
Copy-Item source_code\results\csv\asr_acc_results_part2.csv member_outputs\jiasinan\csv\ -Force
Copy-Item source_code\results\models\backdoor_middle_right.pt member_outputs\jiasinan\models\ -Force
Copy-Item source_code\results\models\backdoor_bottom_left.pt member_outputs\jiasinan\models\ -Force
Copy-Item source_code\results\models\backdoor_bottom_center.pt member_outputs\jiasinan\models\ -Force
Copy-Item source_code\results\models\backdoor_bottom_right.pt member_outputs\jiasinan\models\ -Force
```

陈昱霖检测完后：

```powershell
Copy-Item source_code\results\csv\detection_results.csv member_outputs\chenyulin\csv\ -Force
```

田玉娇合并完后：

```powershell
Copy-Item source_code\results\csv\final_results.csv member_outputs\tianyujiao\csv\ -Force
Copy-Item source_code\results\csv\poison_rate_ablation.csv member_outputs\tianyujiao\csv\ -Force
```

### 提交方式

以李卓尔为例：

```bash
git switch dev
git pull origin dev
git switch -c feature/lizhuoer-part1-results
git add member_outputs/lizhuoer
git commit -m "提交李卓尔五个位置实验结果"
git push -u origin feature/lizhuoer-part1-results
```

其他成员只需要把 `member_outputs/lizhuoer` 换成自己的目录。
