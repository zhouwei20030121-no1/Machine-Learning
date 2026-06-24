import argparse
import csv
from pathlib import Path

from experiments.evaluate_asr import evaluate_asr
from experiments.evaluate_clean_acc import evaluate_clean_accuracy
from experiments.train_backdoor import train_backdoor
from utils.config import BATCH_SIZE, CSV_DIR, EPOCHS, RANDOM_SEED, TARGET_LABEL, ensure_dirs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run poison-rate ablation at a fixed trigger position.")
    parser.add_argument("--position", default="bottom_right")
    parser.add_argument("--rates", nargs="+", type=float, default=[0.05, 0.10, 0.15])
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--target-label", type=int, default=TARGET_LABEL)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--output", default=str(CSV_DIR / "poison_rate_ablation.csv"))
    args = parser.parse_args()

    ensure_dirs()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Poison Rate", "Position", "Clean Accuracy", "ASR", "Epoch", "Training Time", "Model Path"]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rate in args.rates:
            metadata = train_backdoor(
                position=args.position,
                poison_rate=rate,
                epochs=args.epochs,
                batch_size=args.batch_size,
                target_label=args.target_label,
                seed=args.seed,
            )
            clean_acc = evaluate_clean_accuracy(metadata["model_path"], args.batch_size)
            asr = evaluate_asr(metadata["model_path"], args.position, args.batch_size, args.target_label)
            writer.writerow(
                {
                    "Poison Rate": rate,
                    "Position": args.position,
                    "Clean Accuracy": f"{clean_acc:.6f}",
                    "ASR": f"{asr:.6f}",
                    "Epoch": args.epochs,
                    "Training Time": f"{metadata['training_time']:.2f}",
                    "Model Path": metadata["model_path"],
                }
            )
            print(f"rate={rate:.2f} clean_acc={clean_acc:.4f} asr={asr:.4f}")


if __name__ == "__main__":
    main()

