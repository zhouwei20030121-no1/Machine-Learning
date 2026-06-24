import random
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from models.cnn_model import SimpleCNN
from utils.config import (
    BATCH_SIZE,
    CIFAR10_MEAN,
    CIFAR10_STD,
    DATA_DIR,
    LEARNING_RATE,
    RANDOM_SEED,
    get_device,
)


def set_seed(seed: int = RANDOM_SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_transforms(normalize: bool = False):
    steps = [transforms.ToTensor()]
    if normalize:
        steps.append(transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD))
    return transforms.Compose(steps)


def load_cifar10(train: bool, normalize: bool = False):
    return datasets.CIFAR10(
        root=str(DATA_DIR),
        train=train,
        download=True,
        transform=get_transforms(normalize=normalize),
    )


def make_loader(dataset, batch_size: int = BATCH_SIZE, shuffle: bool = False) -> DataLoader:
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=2, pin_memory=True)


def build_model(checkpoint: str | Path | None = None, device: torch.device | None = None) -> SimpleCNN:
    device = device or get_device()
    model = SimpleCNN().to(device)
    if checkpoint:
        state = torch.load(checkpoint, map_location=device)
        model.load_state_dict(state["model_state_dict"] if "model_state_dict" in state else state)
    return model


def train_one_epoch(model, loader, optimizer, criterion, device) -> Tuple[float, float]:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * labels.size(0)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate_accuracy(model, loader, device) -> float:
    model.eval()
    correct = 0
    total = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)
    return correct / total


def make_optimizer(model) -> torch.optim.Optimizer:
    return torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)


def make_criterion() -> nn.Module:
    return nn.CrossEntropyLoss()


def now_seconds() -> float:
    return time.perf_counter()


def elapsed_seconds(start: float) -> float:
    return time.perf_counter() - start


def checkpoint_payload(model, metadata: Dict) -> Dict:
    return {"model_state_dict": model.state_dict(), "metadata": metadata}
