from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# 自动定位项目根目录
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "results" / "csv" / "poison_rate_ablation.csv"
figure_dir = BASE_DIR / "results" / "figures"
figure_dir.mkdir(parents=True, exist_ok=True)

# ==========================
# 读取数据
# ==========================
df = pd.read_csv(csv_path)

# 如果CSV是Tab分隔，自动重新读取
if len(df.columns) == 1:
    df = pd.read_csv(csv_path, sep="\t")

# ==========================
# 排序
# ==========================
df = df.sort_values("Poison Rate")

rates = df["Poison Rate"].astype(float)
clean_acc = df["Clean Accuracy"]
asr = df["ASR"]

# ==========================
# 开始绘图
# ==========================
plt.figure(figsize=(8, 5))

plt.plot(
    rates,
    clean_acc,
    marker='o',
    linewidth=2.5,
    markersize=8,
    label='Clean Accuracy'
)

plt.plot(
    rates,
    asr,
    marker='s',
    linewidth=2.5,
    markersize=8,
    label='ASR'
)

# 标注数据
for x, y in zip(rates, clean_acc):
    plt.text(
        x,
        y + 0.004,
        f"{y:.3f}",
        ha='center',
        fontsize=10
    )

for x, y in zip(rates, asr):
    plt.text(
        x,
        y + 0.004,
        f"{y:.3f}",
        ha='center',
        fontsize=10
    )

plt.xlabel("Poison Rate", fontsize=12)
plt.ylabel("Accuracy / ASR", fontsize=12)

plt.title(
    "Effect of Poison Rate on Clean Accuracy and ASR",
    fontsize=14,
    fontweight='bold'
)

plt.xticks(rates)
plt.ylim(0.70, 1.00)

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()

# ==========================
# 保存图片
# ==========================
save_path = figure_dir / "poison_rate_ablation.png"

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("=" * 60)
print("Figure saved successfully!")
print(save_path)
print("=" * 60)