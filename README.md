# Machine-Learning

## 项目题目

基于 CIFAR-10 的后门攻击触发器位置空间敏感性分析

本项目基于 CIFAR-10 图像分类任务，使用 BadNets 后门攻击方法，在训练集中植入固定的 3x3 白色触发器，并把触发器分别放在图像的 3x3 九个空间位置。通过比较不同位置下模型的 Clean Accuracy、ASR 和防御检测分数，分析触发器空间位置对后门攻击效果和隐蔽性的影响。

## 周玮负责内容

周玮负责项目总体设计、代码框架搭建、核心后门攻击代码实现、主实验分析和运行说明。已经完成的核心内容包括：

- CIFAR-10 数据加载；
- Simple CNN 模型；
- BadNets 训练集投毒；
- 3x3 九个触发器位置；
- 后门模型训练脚本；
- Clean Accuracy 测试脚本；
- ASR 测试脚本；
- 单位置训练与评估入口；
- 统一实验参数配置；
- README 运行说明。

其他成员只需要按照 README 中的命令运行自己负责的位置，并把输出 CSV、模型路径和实验现象交给对应负责人。

## 统一实验参数

| 参数 | 设置 |
|---|---|
| 数据集 | CIFAR-10 |
| 模型 | Simple CNN |
| 攻击方法 | BadNets |
| 触发器 | 3x3 白色方块 |
| 触发器位置 | 3x3 九个位置 |
| 目标类别 | 0 |
| 默认投毒比例 | 0.10 |
| 默认训练轮数 | 10 |
| 优化器 | Adam |
| 学习率 | 0.001 |
| 随机种子 | 2026 |
| 评价指标 | Clean Accuracy、ASR、Detection Score |

注意：跑 9 个位置实验时，只能改变 `--position` 和 `--part`，不要随意改 `epoch`、`poison-rate`、`target-label` 等参数，否则不同位置之间不能公平比较。

## 根目录结构

```text
Machine-Learning/
  README.md                         # 项目总说明，GitHub 首页展示
  任务分工.docx                     # 小组任务分工文档
  时间规划.docx                     # 小组时间规划文档
  03 机器学习-期末题目[1].pdf        # 课程题目说明
  source_code/                      # 代码主目录
```

## 代码目录结构

```text
source_code/
  README.md                         # 详细代码运行说明
  requirements.txt                  # Python 依赖

  models/
    cnn_model.py                    # Simple CNN 模型结构

  utils/
    config.py                       # 统一参数、路径、9 个触发器位置
    trigger_utils.py                # 触发器添加函数
    dataset_poison.py               # BadNets 投毒数据集包装
    train_utils.py                  # 训练、评估、数据加载通用函数

  experiments/
    train_backdoor.py               # 单位置后门模型训练
    evaluate_clean_acc.py           # Clean Accuracy 测试
    evaluate_asr.py                 # ASR 测试
    run_position.py                 # 单位置训练 + 测试 + 写入 CSV
    run_poison_rate_ablation.py     # 投毒比例消融实验

  defense/
    detection_score.py              # 简化 Neural Cleanse 检测分数

  analysis/
    merge_results.py                # 合并 9 个位置结果和检测结果
    plot_results.py                 # 生成基础图表
    visualize_trigger_samples.py    # 生成触发器样本九宫格

  results/
    csv/                            # 输出 CSV 表格
    models/                         # 输出模型权重
    logs/                           # 训练日志

  figures/                          # 输出图表
  test_data/                        # 测试截图、样例数据
```

## 快速开始

进入代码目录：

```bash
cd source_code
```

安装依赖：

```bash
pip install -r requirements.txt
```

跑一个位置：

```bash
python -m experiments.run_position --position top_left --part part1
```

更多命令见 [source_code/README.md](source_code/README.md)。

## 成员交付关系

| 负责人 | 交付内容 | 交给谁 | 用途 |
|---|---|---|---|
| 周玮 | 代码框架、运行命令、统一参数、模型保存规则 | 李卓尔、贾思楠、陈昱霖、田玉娇 | 跑实验、做检测、合并结果 |
| 李卓尔 | 5 个位置实验 CSV、模型、日志、现象说明 | 田玉娇、陈昱霖、周玮 | 合并结果、防御检测、写主实验分析 |
| 贾思楠 | 4 个位置实验 CSV、模型、图表 | 田玉娇、陈昱霖 | 合并结果、防御检测、插入报告 |
| 陈昱霖 | `detection_results.csv`、检测难度说明、权衡分析 | 田玉娇、贾思楠、周玮 | 合并结果、画图、写 4.4/4.5 |
| 田玉娇 | `final_results.csv`、消融结果、最终报告整合 | 贾思楠、周玮 | 画最终图、最终提交 |

## 最终提交材料建议

```text
Machine-Learning/
  source_code/
  figures/
  results/
  test_data/
  课程设计报告.docx
  课程设计报告.pdf
  运行说明.txt
```

## 分支协作规范

仓库现在有两个长期分支：

- `main`：稳定分支，只放最终确认后的内容；
- `dev`：开发基准分支，所有成员后续写代码都先从 `dev` 创建自己的分支。

成员开发流程建议如下：

```bash
git switch dev
git pull origin dev
git switch -c feature/your-name-task
```

示例：

```bash
git switch dev
git pull origin dev
git switch -c feature/lizhuoer-part1-experiments
```

完成自己的代码或结果整理后：

```bash
git add .
git commit -m "描述本次完成的内容"
git push -u origin feature/your-name-task
```

然后在 GitHub 上向 `dev` 分支提交 Pull Request。确认没有问题后，再合并到 `dev`。最终提交前，再由负责人把 `dev` 合并到 `main`。

注意：不要直接在 `main` 上写代码，也不要直接把未检查的实验结果推到 `main`。

## 成员结果提交目录

除了代码目录 `source_code/` 以外，项目还新增了 `member_outputs/`，专门用来放每个成员自己的实验结果和说明文件。

```text
member_outputs/
  README.md                         # 成员交付目录总说明，写明谁交什么、交到哪里

  zhouwei/                          # 周玮：代码框架、统一参数、参考模型和主实验说明
    README.md
    reference_top_left/             # 已完整训练好的 top_left 参考样例
      models/backdoor_top_left.pt   # 参考模型，10 轮训练
      csv/asr_acc_results_reference_top_left.csv
      notes/

  lizhuoer/                         # 李卓尔：5 个位置实验结果
    README.md
    csv/                            # asr_acc_results_part1.csv
    models/                         # top_left/top_center/top_right/middle_left/center 五个模型
    logs/                           # 训练日志
    screenshots/                    # 运行截图或测试截图
    notes/                          # 实验现象说明

  jiasinan/                         # 贾思楠：4 个位置实验结果和最终图表
    README.md
    csv/                            # asr_acc_results_part2.csv
    models/                         # middle_right/bottom_left/bottom_center/bottom_right 四个模型
    logs/
    screenshots/
    figures/                        # ASR 热力图、检测热力图、权衡图等
    notes/                          # 图表说明

  chenyulin/                        # 陈昱霖：防御检测和隐蔽性分析
    README.md
    csv/                            # detection_results.csv
    models_to_check/                # 可放模型路径清单或临时检测说明
    notes/                          # Neural Cleanse 检测难度说明、权衡分析文字

  tianyujiao/                       # 田玉娇：结果合并、消融实验、报告整合
    README.md
    csv/                            # final_results.csv、poison_rate_ablation.csv
    figures/                        # 基础图表或最终整合图表
    report/                         # 最终报告 docx/pdf、运行说明
    notes/                          # 合并检查说明、最终提交材料说明
```

## 实验结果双目录规则

实验结果需要同时保留在两个地方：

1. `source_code/results/`：程序运行目录，训练、检测、合并脚本默认从这里读取和写入。
2. `member_outputs/个人目录/`：成员提交目录，用来归档每个人自己负责的结果，方便检查和提交。

也就是说，大家运行代码后，先让程序自动输出到 `source_code/results/`，然后再把自己负责的 CSV、模型、日志、截图和说明复制到 `member_outputs/自己的目录/`。

例如李卓尔跑完 5 个位置后：

```text
source_code/results/csv/asr_acc_results_part1.csv
source_code/results/models/backdoor_top_left.pt
source_code/results/models/backdoor_top_center.pt
source_code/results/models/backdoor_top_right.pt
source_code/results/models/backdoor_middle_left.pt
source_code/results/models/backdoor_center.pt
```

还要复制一份到：

```text
member_outputs/lizhuoer/csv/asr_acc_results_part1.csv
member_outputs/lizhuoer/models/backdoor_top_left.pt
member_outputs/lizhuoer/models/backdoor_top_center.pt
member_outputs/lizhuoer/models/backdoor_top_right.pt
member_outputs/lizhuoer/models/backdoor_middle_left.pt
member_outputs/lizhuoer/models/backdoor_center.pt
```

周玮已经放了一个完整训练参考样例：

```text
member_outputs/zhouwei/reference_top_left/models/backdoor_top_left.pt
member_outputs/zhouwei/reference_top_left/csv/asr_acc_results_reference_top_left.csv
```

参考指标：

```text
Position: top_left
Clean Accuracy: 0.703700
ASR: 0.940600
Epoch: 10
Training Time: 181.63 秒
```

## 成员提交命令

所有成员都从 `dev` 开自己的分支：

```bash
git switch dev
git pull origin dev
git switch -c feature/你的名字-任务名
```

只提交自己的目录，例如李卓尔：

```bash
git add member_outputs/lizhuoer
git commit -m "提交李卓尔五个位置实验结果"
git push -u origin feature/lizhuoer-part1-results
```

然后在 GitHub 上创建 Pull Request，目标分支选择 `dev`。
