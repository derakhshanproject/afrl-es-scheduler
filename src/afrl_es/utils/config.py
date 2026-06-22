from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
import yaml
from .paths import resolve_path


def load_yaml(path: str | Path) -> dict[str, Any]:
    path = resolve_path(path)
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_article_configs() -> dict[str, Any]:
    simulation = load_yaml('configs/article/simulation.yaml')
    afrl_es = load_yaml('configs/article/afrl_es.yaml')
    refs = load_yaml('configs/article/reference_methods.yaml')
    eval_cfg = load_yaml('configs/article/evaluation.yaml')
    return {
        'simulation': simulation,
        'afrl_es': afrl_es,
        'reference_methods': refs,
        'evaluation': eval_cfg,
    }
