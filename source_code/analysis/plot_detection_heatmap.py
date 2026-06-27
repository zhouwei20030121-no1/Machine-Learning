import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 自动定位当前脚本所在目录
BASE_DIR = Path(__file__).resolve().parent

csv_path = BASE_DIR.parent / "results" / "csv" / "final_results.csv"

print("读取文件：", csv_path)

df = pd.read_csv(csv_path)

# 构建3×3矩阵
position_map = {
    "top_left": (0, 0),
    "top_center": (0, 1),
    "top_right": (0, 2),
    "middle_left": (1, 0),
    "center": (1, 1),
    "middle_right": (1, 2),
    "bottom_left": (2, 0),
    "bottom_center": (2, 1),
    "bottom_right": (2, 2),
}

heatmap = np.zeros((3, 3))

for _, row in df.iterrows():
    r, c = position_map[row["Position"]]
    heatmap[r, c] = row["Detection Score"]

# 绘图
plt.figure(figsize=(8, 6))

im = plt.imshow(
    heatmap,
    cmap="YlOrRd",
    vmin=0.92,
    vmax=1.00
)

# 坐标轴
plt.xticks(
    [0, 1, 2],
    ["Left", "Center", "Right"],
    fontsize=12
)

plt.yticks(
    [0, 1, 2],
    ["Top", "Middle", "Bottom"],
    fontsize=12
)

# 添加数值
for i in range(3):
    for j in range(3):
        plt.text(
            j,
            i,
            f"{heatmap[i,j]:.3f}",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="black"
        )

cbar = plt.colorbar(im)
cbar.set_label("Detection Score", fontsize=12)

plt.title(
    "Detection Score Heatmap of Different Trigger Positions",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "detection_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()