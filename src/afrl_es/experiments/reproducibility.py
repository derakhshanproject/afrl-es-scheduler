from __future__ import annotations
import platform
import sys
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class EnvironmentManifest:
    python_version: str
    platform: str
    implementation: str


def collect_environment_manifest() -> dict:
    return asdict(EnvironmentManifest(
        python_version=sys.version,
        platform=platform.platform(),
        implementation=platform.python_implementation(),
    ))
