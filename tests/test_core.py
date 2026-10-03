import unittest

from duration_humanizer import humanize, humanize_parts


class TestHumanize(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(humanize(0.0), "0s")
        self.assertEqual(humanize(0), "0s")

    def test_plain_seconds(self):
        self.assertEqual(humanize(45.0), "45s")

    def test_minutes_and_seconds(self):
        self.assertEqual(humanize(90.0), "1m30s")

    def test_hours_minutes_seconds(self):
        self.assertEqual(humanize(11565.0), "3h12m45s")

    def test_days_hours_minutes_seconds(self):
        self.assertEqual(humanize(90061.0), "1d1h1m1s")

    def test_one_day(self):
        self.assertEqual(humanize(86400.0), "1d")

    def test_subsecond_truncated(self):
        # Truncation, not rounding: 59.9s is '59s', never '1m'.
        self.assertEqual(humanize(59.9), "59s")

    def test_subsecond_remainder_drops(self):
        self.assertEqual(humanize(1.999), "1s")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            humanize(-1.0)

    def test_parts_returns_list(self):
        self.assertEqual(humanize_parts(11565.0), ["3h", "12m", "45s"])

    def test_parts_zero(self):
        self.assertEqual(humanize_parts(0.0), ["0s"])

    def test_large_value(self):
        # 2 days + 3 hours + 4 minutes + 5 seconds
        self.assertEqual(humanize(2 * 86400 + 3 * 3600 + 4 * 60 + 5), "2d3h4m5s")


if __name__ == "__main__":
    unittest.main()
