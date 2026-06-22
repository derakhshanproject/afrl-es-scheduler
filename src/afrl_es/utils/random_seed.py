from __future__ import annotations
import random
import numpy as np


def set_global_seed(seed: int) -> np.random.Generator:
    random.seed(seed)
    np.random.seed(seed)
    return np.random.default_rng(seed)


def child_seed(base_seed: int, *parts: int) -> int:
    value = int(base_seed)
    for p in parts:
        value = (value * 1103515245 + 12345 + int(p)) & 0x7FFFFFFF
    return value
