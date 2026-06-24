import argparse
from pathlib import Path
from typing import Dict

import torch

from utils.config import (
    BATCH_SIZE,
    EPOCHS,
    MODEL_DIR,
    POISON_RATE,
    RANDOM_SEED,
    TARGET_LABEL,
    ensure_dirs,
    get_device,
    validate_position,
)
from utils.dataset_poison import PoisonedDataset
from utils.train_utils import (
    build_model,
    checkpoint_payload,
    elapsed_seconds,
    load_cifar10,
    make_criterion,
    make_loader,
    make_optimizer,
    now_seconds,
    set_seed,
    train_one_epoch,
)


def train_backdoor(
    position: str,
    poison_rate: float = POISON_RATE,
    epochs: int = EPOCHS,
    batch_size: int = BATCH_SIZE,
    target_label: int = TARGET_LABEL,
    seed: int = RANDOM_SEED,
    model_dir: Path = MODEL_DIR,
) -> Dict:
    validate_position(position)
    ensure_dirs()
    set_seed(seed)

    device = get_device()
    train_set = load_cifar10(train=True)
    poisoned_train = PoisonedDataset(
        train_set,
        position=position,
        poison_rate=poison_rate,
        target_label=target_label,
        seed=seed,
    )
    train_loader = make_loader(poisoned_train, batch_size=batch_size, shuffle=True)

    model = build_model(device=device)
    optimizer = make_optimizer(model)
    criterion = make_criterion()

    start = now_seconds()
    history = []
    for epoch in range(1, epochs + 1):
        loss, acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        history.append({"epoch": epoch, "loss": loss, "train_acc": acc})
        print(f"epoch={epoch:02d} loss={loss:.4f} train_acc={acc:.4f}")

    training_time = elapsed_seconds(start)
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"backdoor_{position}.pt"
    metadata = {
        "position": position,
        "poison_rate": poison_rate,
        "epochs": epochs,
        "batch_size": batch_size,
        "target_label": target_label,
        "seed": seed,
        "training_time": training_time,
        "history": history,
    }
    torch.save(checkpoint_payload(model, metadata), model_path)
    metadata["model_path"] = str(model_path)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Train one BadNets backdoor model for a trigger position.")
    parser.add_argument("--position", required=True)
    parser.add_argument("--poison-rate", type=float, default=POISON_RATE)
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--target-label", type=int, default=TARGET_LABEL)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()

    metadata = train_backdoor(
        position=args.position,
        poison_rate=args.poison_rate,
        epochs=args.epochs,
        batch_size=args.batch_size,
        target_label=args.target_label,
        seed=args.seed,
    )
    print(f"Saved model: {metadata['model_path']}")


if __name__ == "__main__":
    main()

