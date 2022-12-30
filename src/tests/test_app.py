import unittest
from src.new_script import DateRange, Date, TimeRange, WeekTimes
from datetime import datetime, timedelta


class TestDateRangeClass(unittest.TestCase):
    def test_str_to_date_returns_right_date(self):

        start = "01/02/2022 10:01:02"
        end = "01/04/2022 10:01:02"

        date_obj = DateRange((start, end))

        self.assertEqual(str(date_obj.start), "2022-02-01 10:01:02")
        self.assertEqual(str(date_obj.end), "2022-04-01 10:01:02")

    def test_error_if_end_before_start(self):

        end = "01/02/2022 10:01:02"
        start = "01/04/2022 10:01:02"

        with self.assertRaises(ValueError):
            date_obj = DateRange((start, end))

    def test_true_if_date_query_between_dates(self):

        start = "01/02/2022 10:01:02"
        end = "01/04/2022 10:01:02"

        date_obj = DateRange((start, end))

        format = "%d/%m/%Y %H:%M:%S"
        between = date_obj.is_between(datetime.strptime("01/02/2022 10:01:02", format))
        before = date_obj.is_between(datetime.strptime("01/02/2021 10:01:02", format))
        after = date_obj.is_between(datetime.strptime("01/02/2023 10:01:02", format))
        on_start = date_obj.is_between(date_obj.start)
        on_end = date_obj.is_between(date_obj.end)

        self.assertTrue(between, "Should be true if between dates.")
        self.assertFalse(before, "Should be false if before start")
        self.assertFalse(after, "Should be false if after end.")
        self.assertTrue(on_start, "Should be true if on start time")
        self.assertTrue(on_end, "Should be true if on end time.")


class TestDateClass(unittest.TestCase):
    def test_datetime_returned(self):

        obj = Date("01/02/2022")

        self.assertIsInstance(obj.date, datetime)

    def test_datetime_time_is_zero(self):

        obj = Date("01/02/2022 01:02:01", format="%d/%m/%Y %H:%M:%S")

        self.assertEqual(obj.date.hour, 0)
        self.assertEqual(obj.date.minute, 0)
        self.assertEqual(obj.date.second, 0)
        self.assertEqual(obj.date.microsecond, 0)


class TestTimeRangeClass(unittest.TestCase):
    def test_str_to_date_returns_right_date(self):

        start = "09:00:00"
        end = "17:01:02"

        date_obj = TimeRange((start, end))

        self.assertEqual(str(date_obj.start.time()), start)
        self.assertEqual(str(date_obj.end.time()), end)

    def test_error_if_end_before_start(self):

        start = "17:00:00"
        end = "09:01:02"

        with self.assertRaises(ValueError):
            TimeRange((start, end))

    def test_true_if_date_query_between_dates(self):

        start = "09:00:00"
        end = "17:01:02"

        date_obj = TimeRange((start, end))

        format = "%H:%M:%S"
        between = date_obj.is_between(datetime.strptime("10:00:00", format))
        before = date_obj.is_between(datetime.strptime("02:30:00", format))
        after = date_obj.is_between(datetime.strptime("23:00:00", format))
        on_start = date_obj.is_between(date_obj.start)
        on_end = date_obj.is_between(date_obj.end)

        self.assertTrue(between, "Should be true if between dates.")
        self.assertFalse(before, "Should be false if before start")
        self.assertFalse(after, "Should be false if after end.")
        self.assertTrue(on_start, "Should be true if on start time")
        self.assertTrue(on_end, "Should be true if on end time.")


class TestWeekTimesClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.start = "09:00:00"
        cls.end = "19:00:00"
        cls.valid_times = [
            datetime.strptime(f"{x:02d}:00:00", "%H:%M:%S") for x in [9, 12, 15, 18]
        ]
        cls.invalid_times = [
            datetime.strptime(f"{x:02d}:00:00", "%H:%M:%S") for x in [5, 6, 20, 23]
        ]

    def test_instantiation(self):
        week = WeekTimes(("09:00:00", "19:00:00"))

        self.assertIsInstance(week.time_range, TimeRange)

        self.assertTrue(all([isinstance(x, bool) for x in week.weekdays]))

    def test_error_if_wrong_number_of_weekdays(self):
        weekdays = [True, True]

        with self.assertRaises(ValueError):
            WeekTimes((self.start, self.end), weekdays=weekdays)

    def test_all_use_default_time(self):
        """If no weekdays are given. All days should use default time range."""

        week = WeekTimes((self.start, self.end))

        for time in self.valid_times:
            for i in range(7):
                offset = (time.weekday() - i) % 7
                new_time = time - timedelta(days=offset)
                self.assertTrue(week.is_valid_time(new_time))

        for time in self.invalid_times:
            for i in range(7):
                offset = (time.weekday() - i) % 7
                new_time = time - timedelta(days=offset)
                self.assertFalse(week.is_valid_time(new_time))

    def test_setting_values_sets_correctly(self):
        days = [
            True,
            ("06:00:00", "08:00:00"),
            False,
            ("09:00:00", "17:30:00"),
            True,
            True,
            True,
        ]
        week = WeekTimes((self.start, self.end), weekdays=days)

        weekdays = week.weekdays

        self.assertTrue(weekdays[0])

        self.assertIsInstance(
            weekdays[1], TimeRange, f"Should be TimeRange, not '{type(weekdays[1])}'"
        )
        self.assertEqual(str(weekdays[1].start.time()), days[1][0])
        self.assertEqual(str(weekdays[1].end.time()), days[1][1])

        self.assertFalse(weekdays[2])

        self.assertIsInstance(
            weekdays[3], TimeRange, f"Should be TimeRange, not '{type(weekdays[3])}'"
        )
        self.assertEqual(str(weekdays[3].start.time()), days[3][0])
        self.assertEqual(str(weekdays[3].end.time()), days[3][1])

        self.assertTrue(weekdays[4])
        self.assertTrue(weekdays[5])
        self.assertTrue(weekdays[6])

    def test_setting_day_to_false_always_invalid_time(self):
        days = [True, False, True, True, False, True, True]
        week = WeekTimes((self.start, self.end), weekdays=days)

        for time in self.valid_times:
            for i in range(7):
                offset = (time.weekday() - i) % 7
                new_time = time - timedelta(days=offset)

                if i in [1, 4]:
                    self.assertFalse(week.is_valid_time(new_time))
                else:
                    self.assertTrue(week.is_valid_time(new_time))

        for time in self.invalid_times:
            for i in range(7):
                offset = (time.weekday() - i) % 7
                new_time = time - timedelta(days=offset)
                self.assertFalse(week.is_valid_time(new_time))

    def test_setting_day_time_range_doesnt_use_default(self):
        days = [True, ["06:00:00", "08:00:00"], True, True, True, True, True]
        week = WeekTimes((self.start, self.end), weekdays=days)

        for time in self.valid_times:
            for i in range(7):
                offset = (time.weekday() - i) % 7
                new_time = time - timedelta(days=offset)

                if i == 1:
                    self.assertFalse(week.is_valid_time(new_time))
                else:
                    self.assertTrue(week.is_valid_time(new_time))

        for time in self.invalid_times:
            for i in range(7):
                if 1 != 1:
                    offset = (time.weekday() - i) % 7
                    new_time = time - timedelta(days=offset)
                    self.assertFalse(week.is_valid_time(new_time))

        good_time = datetime.strptime("07:00:00", "%H:%M:%S")
        offset = (good_time.weekday() - 1) % 7
        new_time = good_time - timedelta(days=offset)

        self.assertTrue(week.is_valid_time(new_time))


if __name__ == "__main__":
    unittest.main()
