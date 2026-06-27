import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 自动定位当前脚本所在目录
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "results" / "csv" / "final_results.csv"

print(f"Reading file: {csv_path}")
df = pd.read_csv(csv_path)

# 名称缩写
short_name = {
    "top_left": "TL", "top_center": "TC", "top_right": "TR",
    "middle_left": "ML", "center": "C", "middle_right": "MR",
    "bottom_left": "BL", "bottom_center": "BC", "bottom_right": "BR"
}

# 💡 核心救急逻辑：为严重重叠的点手动设置 (x偏移, y偏移)
# 默认偏移是 (5, 5)，我们把挤在一起的往相反方向推
manual_offsets = {
    "center": (-15, 12),       # C 往左上角推
    "middle_right": (12, -15), # MR 往右下角推
    "bottom_left": (-15, 10),  # BL 往左上角推
    "bottom_right": (12, -10)  # BR 往右下角推
}

plt.figure(figsize=(8, 6), dpi=120)

plt.scatter(
    df["ASR"],
    df["Detection Score"],
    s=150, 
    alpha=0.8, 
    edgecolors='white',
    linewidth=1.5,
    zorder=3
)

# 添加标签，应用手动偏移
for _, row in df.iterrows():
    pos_name = row["Position"]
    # 如果在字典里就用字典设定的偏移，否则用默认的 (5, 5)
    offset = manual_offsets.get(pos_name, (5, 5))
    
    plt.annotate(
        short_name[pos_name],
        (row["ASR"], row["Detection Score"]),
        xytext=offset,
        textcoords="offset points",
        fontsize=11,
        fontweight="bold"
    )

plt.xlabel("Attack Success Rate (ASR)", fontsize=12)
plt.ylabel("Detection Score", fontsize=12)
plt.title("Trade-off Between ASR and Detection Score", fontsize=14, fontweight="bold", pad=15)

plt.grid(linestyle="--", alpha=0.4, zorder=0)

plt.xlim(0.91, 1.01)
plt.ylim(0.91, 1.01)
plt.tight_layout()

# 保存
save_path = BASE_DIR.parent / "figures" / "asr_detection_tradeoff.png"
save_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(save_path, dpi=300, bbox_inches="tight")
print("Success: Chart saved successfully!")

plt.show()