from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen


@dataclass(frozen=True)
class AqiReading:
    city_name: str
    aqi: int
    url: str | None


class WaqiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token

    def fetch_city_aqi(self, city: str) -> AqiReading:
        city_path = quote(city.strip(), safe="")
        query = urlencode({"token": self._token})
        url = f"{self._base_url}/{city_path}/?{query}"

        try:
            with urlopen(url, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise RuntimeError(f"WAQI request failed with HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"WAQI request failed: {exc.reason}") from exc

        return _parse_reading(payload)


def _parse_reading(payload: dict[str, Any]) -> AqiReading:
    if payload.get("status") != "ok":
        message = payload.get("data") or payload.get("message") or "unknown error"
        raise RuntimeError(f"WAQI API returned non-ok status: {message}")

    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("WAQI API response does not contain a data object")

    raw_aqi = data.get("aqi")
    try:
        aqi = int(raw_aqi)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"WAQI API returned invalid AQI value: {raw_aqi!r}") from exc

    city = data.get("city")
    city_name = "Unknown"
    city_url = None
    if isinstance(city, dict):
        raw_name = city.get("name")
        raw_url = city.get("url")
        if isinstance(raw_name, str) and raw_name:
            city_name = raw_name
        if isinstance(raw_url, str) and raw_url:
            city_url = raw_url

    return AqiReading(city_name=city_name, aqi=aqi, url=city_url)

