import torch

from utils.config import POSITIONS, TRIGGER_SIZE, TRIGGER_VALUE, validate_position


def add_trigger(image: torch.Tensor, position: str, trigger_value: float = TRIGGER_VALUE) -> torch.Tensor:
    """Return a copy of a CHW image tensor with a square BadNets trigger."""
    validate_position(position)
    if image.ndim != 3:
        raise ValueError("Expected image tensor with shape [C, H, W].")

    poisoned = image.clone()
    row, col = POSITIONS[position]
    poisoned[:, row : row + TRIGGER_SIZE, col : col + TRIGGER_SIZE] = trigger_value
    return poisoned


def add_trigger_batch(images: torch.Tensor, position: str, trigger_value: float = TRIGGER_VALUE) -> torch.Tensor:
    """Return a copy of an NCHW batch with the trigger added to every image."""
    validate_position(position)
    if images.ndim != 4:
        raise ValueError("Expected image batch with shape [N, C, H, W].")

    poisoned = images.clone()
    row, col = POSITIONS[position]
    poisoned[:, :, row : row + TRIGGER_SIZE, col : col + TRIGGER_SIZE] = trigger_value
    return poisoned

