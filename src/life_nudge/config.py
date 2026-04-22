from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    waqi_feed_base_url: str
    waqi_token: str
    city: str
    bark_url: str
    check_interval_seconds: int
    state_file: Path


def load_config() -> Config:
    waqi_token = _required_env("WAQI_TOKEN")
    bark_url = _required_env("BARK_URL")

    return Config(
        waqi_feed_base_url=os.getenv("WAQI_FEED_BASE_URL", "https://api.waqi.info/feed"),
        waqi_token=waqi_token,
        city=os.getenv("AQI_CITY", "beijing"),
        bark_url=bark_url,
        check_interval_seconds=_int_env("AQI_CHECK_INTERVAL_SECONDS", 600),
        state_file=Path(os.getenv("AQI_STATE_FILE", ".aqi_state.json")),
    )


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer") from exc
    if parsed <= 0:
        raise RuntimeError(f"Environment variable {name} must be greater than 0")
    return parsed

