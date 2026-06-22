from __future__ import annotations


def artifact_name(metric: str, sweep_name: str, scope: str = 'method_comparison', extension: str = 'png') -> str:
    return f"{metric}__by__{sweep_name}__{scope}.{extension}"
