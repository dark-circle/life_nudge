from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class BarkNotifier:
    def __init__(self, bark_url: str) -> None:
        self._bark_url = bark_url

    def send(self, title: str, body: str) -> None:
        payload = json.dumps({"title": title, "body": body}).encode("utf-8")
        request = Request(
            self._bark_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=20) as response:
                response.read()
        except HTTPError as exc:
            raise RuntimeError(f"Bark request failed with HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"Bark request failed: {exc.reason}") from exc

