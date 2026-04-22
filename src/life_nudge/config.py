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
    load_dotenv()

    waqi_token = os.getenv("WAQI_TOKEN") or _required_env("WAQI_TOKEN")
    bark_url = os.getenv("BARK_URL") or _required_env("BARK_URL")

    return Config(
        waqi_feed_base_url=os.getenv("WAQI_FEED_BASE_URL", "https://api.waqi.info/feed"),
        waqi_token=waqi_token,
        city=os.getenv("AQI_CITY", "beijing"),
        bark_url=bark_url,
        check_interval_seconds=_int_env("AQI_CHECK_INTERVAL_SECONDS", 600),
        state_file=Path(os.getenv("AQI_STATE_FILE", "src/data/aqi_state.json")),
    )


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or _find_dotenv()
    if env_path is None or not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        key_value = _parse_env_line(line)
        if key_value is None:
            continue
        key, value = key_value
        os.environ.setdefault(key, value)


def _find_dotenv() -> Path | None:
    search_roots = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parents[2]]
    for root in search_roots:
        env_path = root / ".env"
        if env_path.exists():
            return env_path
    return None


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None

    key, value = stripped.split("=", 1)
    key = key.strip()
    if not key:
        return None

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]

    return key, value


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
