import argparse
import csv
from pathlib import Path

from experiments.evaluate_asr import evaluate_asr
from experiments.evaluate_clean_acc import evaluate_clean_accuracy
from experiments.train_backdoor import train_backdoor
from utils.config import BATCH_SIZE, CSV_DIR, EPOCHS, POISON_RATE, RANDOM_SEED, TARGET_LABEL, ensure_dirs


def append_result(csv_path: Path, row: dict) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Position", "Clean Accuracy", "ASR", "Epoch", "Training Time", "Model Path", "Note"]
    exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and evaluate one trigger position.")
    parser.add_argument("--position", required=True)
    parser.add_argument("--part", choices=["part1", "part2", "scratch"], default="scratch")
    parser.add_argument("--poison-rate", type=float, default=POISON_RATE)
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--target-label", type=int, default=TARGET_LABEL)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    ensure_dirs()
    metadata = train_backdoor(
        position=args.position,
        poison_rate=args.poison_rate,
        epochs=args.epochs,
        batch_size=args.batch_size,
        target_label=args.target_label,
        seed=args.seed,
    )
    model_path = metadata["model_path"]
    clean_acc = evaluate_clean_accuracy(model_path, args.batch_size)
    asr = evaluate_asr(model_path, args.position, args.batch_size, args.target_label)

    output_name = {
        "part1": "asr_acc_results_part1.csv",
        "part2": "asr_acc_results_part2.csv",
        "scratch": "asr_acc_results_scratch.csv",
    }[args.part]
    append_result(
        CSV_DIR / output_name,
        {
            "Position": args.position,
            "Clean Accuracy": f"{clean_acc:.6f}",
            "ASR": f"{asr:.6f}",
            "Epoch": args.epochs,
            "Training Time": f"{metadata['training_time']:.2f}",
            "Model Path": model_path,
            "Note": args.note,
        },
    )
    print(f"position={args.position} clean_acc={clean_acc:.4f} asr={asr:.4f}")


if __name__ == "__main__":
    main()

