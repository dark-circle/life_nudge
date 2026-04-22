import os
import tempfile
import unittest
from pathlib import Path

from life_nudge.config import load_dotenv


class LoadDotenvTest(unittest.TestCase):
    def test_loads_env_file_without_overriding_existing_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "WAQI_TOKEN=file-token",
                        'BARK_URL="https://example.com/bark"',
                        "EXISTING_VALUE=from-file",
                    ]
                ),
                encoding="utf-8",
            )

            old_values = {key: os.environ.get(key) for key in ["WAQI_TOKEN", "BARK_URL", "EXISTING_VALUE"]}
            try:
                os.environ["EXISTING_VALUE"] = "from-env"
                os.environ.pop("WAQI_TOKEN", None)
                os.environ.pop("BARK_URL", None)

                load_dotenv(env_path)

                self.assertEqual(os.environ["WAQI_TOKEN"], "file-token")
                self.assertEqual(os.environ["BARK_URL"], "https://example.com/bark")
                self.assertEqual(os.environ["EXISTING_VALUE"], "from-env")
            finally:
                for key, value in old_values.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
