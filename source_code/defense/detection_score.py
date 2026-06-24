import argparse
import csv
from pathlib import Path

import torch
import torch.nn.functional as F

from utils.config import BATCH_SIZE, CSV_DIR, POISON_RATE, TARGET_LABEL, TRIGGER_SIZE, get_device, validate_position
from utils.dataset_poison import PoisonedDataset
from utils.train_utils import build_model, load_cifar10, make_loader


def classify_difficulty(score: float) -> str:
    if score >= 0.80:
        return "Low Detection Difficulty"
    if score >= 0.50:
        return "Medium Detection Difficulty"
    return "High Detection Difficulty"


@torch.no_grad()
def compute_detection_score(
    model_path: str,
    position: str,
    batch_size: int = BATCH_SIZE,
    target_label: int = TARGET_LABEL,
) -> dict:
    validate_position(position)
    device = get_device()
    model = build_model(model_path, device=device)
    model.eval()

    test_set = load_cifar10(train=False)
    triggered_set = PoisonedDataset(
        test_set,
        position=position,
        poison_rate=POISON_RATE,
        target_label=target_label,
        poison_all=True,
    )
    loader = make_loader(triggered_set, batch_size=batch_size, shuffle=False)

    confidence_sum = 0.0
    total = 0
    for images, _ in loader:
        images = images.to(device)
        probs = F.softmax(model(images), dim=1)
        confidence_sum += probs[:, target_label].sum().item()
        total += images.size(0)

    detection_score = confidence_sum / total
    mask_norm = (TRIGGER_SIZE * TRIGGER_SIZE) / (32 * 32)
    return {
        "Position": position,
        "Detection Score": f"{detection_score:.6f}",
        "Mask Norm": f"{mask_norm:.6f}",
        "Detection Difficulty": classify_difficulty(detection_score),
        "Model Path": model_path,
    }


def write_detection_result(row: dict, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Position", "Detection Score", "Mask Norm", "Detection Difficulty", "Model Path"]
    exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute simplified Neural Cleanse detection score.")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--position", required=True)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--target-label", type=int, default=TARGET_LABEL)
    parser.add_argument("--output", default=str(CSV_DIR / "detection_results.csv"))
    args = parser.parse_args()

    row = compute_detection_score(args.model_path, args.position, args.batch_size, args.target_label)
    write_detection_result(row, Path(args.output))
    print(row)


if __name__ == "__main__":
    main()

