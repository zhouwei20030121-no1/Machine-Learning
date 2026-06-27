from pathlib import Path

import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
CSV_DIR = RESULTS_DIR / "csv"
MODEL_DIR = RESULTS_DIR / "models"
LOG_DIR = RESULTS_DIR / "logs"
FIGURE_DIR = RESULTS_DIR / "figures"

IMAGE_SIZE = 32
NUM_CLASSES = 10
TRIGGER_SIZE = 3
TRIGGER_VALUE = 1.0

TARGET_LABEL = 0
POISON_RATE = 0.10
EPOCHS = 10
BATCH_SIZE = 128
LEARNING_RATE = 0.001
RANDOM_SEED = 2026

POSITIONS = {
    "top_left": (0, 0),
    "top_center": (0, (IMAGE_SIZE - TRIGGER_SIZE) // 2),
    "top_right": (0, IMAGE_SIZE - TRIGGER_SIZE),
    "middle_left": ((IMAGE_SIZE - TRIGGER_SIZE) // 2, 0),
    "center": ((IMAGE_SIZE - TRIGGER_SIZE) // 2, (IMAGE_SIZE - TRIGGER_SIZE) // 2),
    "middle_right": ((IMAGE_SIZE - TRIGGER_SIZE) // 2, IMAGE_SIZE - TRIGGER_SIZE),
    "bottom_left": (IMAGE_SIZE - TRIGGER_SIZE, 0),
    "bottom_center": (IMAGE_SIZE - TRIGGER_SIZE, (IMAGE_SIZE - TRIGGER_SIZE) // 2),
    "bottom_right": (IMAGE_SIZE - TRIGGER_SIZE, IMAGE_SIZE - TRIGGER_SIZE),
}

POSITION_ORDER = list(POSITIONS.keys())

CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2470, 0.2435, 0.2616)


def ensure_dirs() -> None:
    for path in [DATA_DIR, CSV_DIR, MODEL_DIR, LOG_DIR, FIGURE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def validate_position(position: str) -> str:
    if position not in POSITIONS:
        valid = ", ".join(POSITION_ORDER)
        raise ValueError(f"Unknown position '{position}'. Valid positions: {valid}")
    return position

