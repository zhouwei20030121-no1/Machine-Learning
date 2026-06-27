import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from utils.config import CSV_DIR, FIGURE_DIR, POSITION_ORDER


GRID_POSITIONS = [
    ["top_left", "top_center", "top_right"],
    ["middle_left", "center", "middle_right"],
    ["bottom_left", "bottom_center", "bottom_right"],
]


def grid_values(df: pd.DataFrame, column: str):
    lookup = dict(zip(df["Position"], df[column]))
    return [[float(lookup[p]) for p in row] for row in GRID_POSITIONS]


def save_heatmap(df: pd.DataFrame, column: str, title: str, output: Path) -> None:
    values = grid_values(df, column)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(values, cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(3), labels=["left", "center", "right"])
    ax.set_yticks(range(3), labels=["top", "middle", "bottom"])
    ax.set_title(title)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{values[i][j]:.2f}", ha="center", va="center", color="white")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def save_acc_asr_bar(df: pd.DataFrame, output: Path) -> None:
    x = range(len(df))
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar([i - 0.2 for i in x], df["Clean Accuracy"], width=0.4, label="Clean Accuracy")
    ax.bar([i + 0.2 for i in x], df["ASR"], width=0.4, label="ASR")
    ax.set_xticks(list(x), df["Position"], rotation=35, ha="right")
    ax.set_ylim(0, 1)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate basic figures from final_results.csv.")
    parser.add_argument("--input", default=str(CSV_DIR / "final_results.csv"))
    parser.add_argument("--output-dir", default=str(FIGURE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    df["Position"] = pd.Categorical(df["Position"], categories=POSITION_ORDER, ordered=True)
    df = df.sort_values("Position")

    save_heatmap(df, "ASR", "ASR Heatmap", output_dir / "asr_heatmap_basic.png")
    save_heatmap(df, "Detection Score", "Detection Difficulty Heatmap", output_dir / "detection_heatmap_basic.png")
    save_acc_asr_bar(df, output_dir / "acc_asr_bar_basic.png")
    print(f"Figures saved to {output_dir}")


if __name__ == "__main__":
    main()

