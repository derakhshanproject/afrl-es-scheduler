from __future__ import annotations
from pathlib import Path
from typing import Any
import json
import pandas as pd
from .paths import resolve_path


def write_json(path: str | Path, data: Any) -> Path:
    p = resolve_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return p


def write_dataframe(path: str | Path, df: pd.DataFrame) -> Path:
    p = resolve_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.csv':
        df.to_csv(p, index=False)
    elif p.suffix.lower() in {'.xlsx', '.xls'}:
        df.to_excel(p, index=False)
    elif p.suffix.lower() == '.json':
        df.to_json(p, orient='records', indent=2)
    else:
        raise ValueError(f"Unsupported dataframe output: {p}")
    return p
