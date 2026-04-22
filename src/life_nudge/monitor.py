from __future__ import annotations

from dataclasses import dataclass

from .notifier import BarkNotifier
from .state import load_state, save_state
from .waqi import WaqiClient


THRESHOLD = 50


@dataclass(frozen=True)
class CheckResult:
    current_aqi: int
    previous_aqi: int | None
    notification_sent: bool
    message: str


class AqiMonitor:
    def __init__(
        self,
        waqi_client: WaqiClient,
        notifier: BarkNotifier,
        city: str,
        state_file,
    ) -> None:
        self._waqi_client = waqi_client
        self._notifier = notifier
        self._city = city
        self._state_file = state_file

    def check_once(self) -> CheckResult:
        reading = self._waqi_client.fetch_city_aqi(self._city)
        state = load_state(self._state_file)
        previous_aqi = state.previous_aqi

        transition = _detect_transition(previous_aqi, reading.aqi)
        notification_sent = False
        message = f"{reading.city_name} AQI 当前值 {reading.aqi}"

        if transition is not None:
            title = f"北京 AQI {transition}"
            body = f"{reading.city_name} AQI 从 {previous_aqi} 变化到 {reading.aqi}，空气质量{transition}。"
            if reading.url:
                body = f"{body}\n{reading.url}"
            self._notifier.send(title=title, body=body)
            notification_sent = True
            message = body

        save_state(self._state_file, reading.aqi)
        return CheckResult(
            current_aqi=reading.aqi,
            previous_aqi=previous_aqi,
            notification_sent=notification_sent,
            message=message,
        )


def _detect_transition(previous_aqi: int | None, current_aqi: int) -> str | None:
    if previous_aqi is None:
        return None
    if current_aqi < THRESHOLD and previous_aqi > THRESHOLD:
        return "变好"
    if current_aqi > THRESHOLD and previous_aqi < THRESHOLD:
        return "变差"
    return None

