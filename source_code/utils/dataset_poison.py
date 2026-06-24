import random
from typing import Iterable, Optional, Set

import torch
from torch.utils.data import Dataset

from utils.config import RANDOM_SEED, TARGET_LABEL
from utils.trigger_utils import add_trigger


def choose_poison_indices(
    labels: Iterable[int],
    poison_rate: float,
    target_label: int = TARGET_LABEL,
    seed: int = RANDOM_SEED,
) -> Set[int]:
    if not 0 <= poison_rate <= 1:
        raise ValueError("poison_rate must be in [0, 1].")

    candidates = [idx for idx, label in enumerate(labels) if int(label) != target_label]
    count = int(len(candidates) * poison_rate)
    rng = random.Random(seed)
    return set(rng.sample(candidates, count))


class PoisonedDataset(Dataset):
    """BadNets-style wrapper: selected non-target samples get a trigger and target label."""

    def __init__(
        self,
        base_dataset: Dataset,
        position: str,
        poison_rate: float,
        target_label: int = TARGET_LABEL,
        seed: int = RANDOM_SEED,
        poison_indices: Optional[Set[int]] = None,
        poison_all: bool = False,
    ) -> None:
        self.base_dataset = base_dataset
        self.position = position
        self.poison_rate = poison_rate
        self.target_label = target_label
        self.poison_all = poison_all

        labels = getattr(base_dataset, "targets", None)
        if labels is None:
            labels = [base_dataset[i][1] for i in range(len(base_dataset))]
        self.poison_indices = poison_indices or choose_poison_indices(labels, poison_rate, target_label, seed)

    def __len__(self) -> int:
        return len(self.base_dataset)

    def __getitem__(self, index: int):
        image, label = self.base_dataset[index]
        if not isinstance(image, torch.Tensor):
            raise TypeError("Base dataset must return tensor images. Put transforms.ToTensor() before this wrapper.")

        if self.poison_all or index in self.poison_indices:
            return add_trigger(image, self.position), self.target_label
        return image, label

