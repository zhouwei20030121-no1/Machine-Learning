import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from utils.config import FIGURE_DIR, POSITION_ORDER
from utils.train_utils import load_cifar10
from utils.trigger_utils import add_trigger


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize one CIFAR-10 sample with triggers in all 9 positions.")
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--output", default=str(FIGURE_DIR / "trigger_samples_grid.png"))
    args = parser.parse_args()

    dataset = load_cifar10(train=False)
    image, _ = dataset[args.index]

    fig, axes = plt.subplots(3, 3, figsize=(6, 6))
    for ax, position in zip(axes.flatten(), POSITION_ORDER):
        poisoned = add_trigger(image, position).permute(1, 2, 0).numpy()
        ax.imshow(poisoned)
        ax.set_title(position, fontsize=8)
        ax.axis("off")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
