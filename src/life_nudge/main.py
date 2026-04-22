from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from life_nudge.config import load_config
from life_nudge.monitor import AqiMonitor
from life_nudge.notifier import BarkNotifier
from life_nudge.waqi import WaqiClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor Beijing AQI and notify via Bark.")
    parser.add_argument("--once", action="store_true", help="Run one check and exit.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    config = load_config()
    monitor = AqiMonitor(
        waqi_client=WaqiClient(config.waqi_feed_base_url, config.waqi_token),
        notifier=BarkNotifier(config.bark_url),
        city=config.city,
        state_file=config.state_file,
    )
    while True:
        try:
            result = monitor.check_once()
            logging.info(
                "AQI check completed: current=%s previous=%s notified=%s message=%s",
                result.current_aqi,
                result.previous_aqi,
                result.notification_sent,
                result.message,
            )
        except Exception:
            logging.exception("AQI check failed")

        if args.once:
            break
        time.sleep(config.check_interval_seconds)


if __name__ == "__main__":
    main()
