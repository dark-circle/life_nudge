import unittest

from life_nudge.monitor import _detect_transition


class DetectTransitionTest(unittest.TestCase):
    def test_detects_aqi_getting_better(self) -> None:
        self.assertEqual(_detect_transition(previous_aqi=60, current_aqi=40), "变好")

    def test_detects_aqi_getting_worse(self) -> None:
        self.assertEqual(_detect_transition(previous_aqi=40, current_aqi=60), "变差")

    def test_does_not_notify_when_equal_to_threshold(self) -> None:
        self.assertIsNone(_detect_transition(previous_aqi=40, current_aqi=50))
        self.assertIsNone(_detect_transition(previous_aqi=60, current_aqi=50))

    def test_does_not_notify_without_previous_value(self) -> None:
        self.assertIsNone(_detect_transition(previous_aqi=None, current_aqi=60))


if __name__ == "__main__":
    unittest.main()
