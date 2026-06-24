import argparse

from utils.config import BATCH_SIZE, get_device
from utils.train_utils import build_model, evaluate_accuracy, load_cifar10, make_loader


def evaluate_clean_accuracy(model_path: str, batch_size: int = BATCH_SIZE) -> float:
    device = get_device()
    test_set = load_cifar10(train=False)
    test_loader = make_loader(test_set, batch_size=batch_size, shuffle=False)
    model = build_model(model_path, device=device)
    return evaluate_accuracy(model, test_loader, device)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate clean accuracy on CIFAR-10 test set.")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()

    acc = evaluate_clean_accuracy(args.model_path, args.batch_size)
    print(f"Clean Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()

