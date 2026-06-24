import argparse

from utils.config import BATCH_SIZE, POISON_RATE, TARGET_LABEL, get_device, validate_position
from utils.dataset_poison import PoisonedDataset
from utils.train_utils import build_model, evaluate_accuracy, load_cifar10, make_loader


def evaluate_asr(
    model_path: str,
    position: str,
    batch_size: int = BATCH_SIZE,
    target_label: int = TARGET_LABEL,
) -> float:
    validate_position(position)
    device = get_device()
    clean_test_set = load_cifar10(train=False)
    triggered_test_set = PoisonedDataset(
        clean_test_set,
        position=position,
        poison_rate=POISON_RATE,
        target_label=target_label,
        poison_all=True,
    )
    loader = make_loader(triggered_test_set, batch_size=batch_size, shuffle=False)
    model = build_model(model_path, device=device)
    return evaluate_accuracy(model, loader, device)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate attack success rate on triggered CIFAR-10 test set.")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--position", required=True)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--target-label", type=int, default=TARGET_LABEL)
    args = parser.parse_args()

    asr = evaluate_asr(args.model_path, args.position, args.batch_size, args.target_label)
    print(f"ASR: {asr:.4f}")


if __name__ == "__main__":
    main()

