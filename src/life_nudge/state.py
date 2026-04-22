from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import time


@dataclass(frozen=True)
class AqiState:
    previous_aqi: int | None


def load_state(path: Path) -> AqiState:
    if not path.exists():
        return AqiState(previous_aqi=None)

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AqiState(previous_aqi=None)

    previous_aqi = payload.get("previous_aqi")
    if not isinstance(previous_aqi, int):
        return AqiState(previous_aqi=None)

    return AqiState(previous_aqi=previous_aqi)


def save_state(path: Path, aqi: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "previous_aqi": aqi,
        "updated_at": int(time()),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

