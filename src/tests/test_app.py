import unittest
from src.new_script import DateRange, Date, TimeRange
from datetime import datetime


class TestDateRangeClass(unittest.TestCase):
    def test_str_to_date_returns_right_date(self):

        start = "01/02/2022 10:01:02"
        end = "01/04/2022 10:01:02"

        date_obj = DateRange(start, end)

        self.assertEqual(str(date_obj.start), "2022-02-01 10:01:02")
        self.assertEqual(str(date_obj.end), "2022-04-01 10:01:02")

    def test_error_if_end_before_start(self):

        end = "01/02/2022 10:01:02"
        start = "01/04/2022 10:01:02"

        with self.assertRaises(ValueError):
            date_obj = DateRange(start, end)

    def test_true_if_date_query_between_dates(self):

        start = "01/02/2022 10:01:02"
        end = "01/04/2022 10:01:02"

        date_obj = DateRange(start, end)

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

        date_obj = TimeRange(start, end)

        self.assertEqual(str(date_obj.start.time()), start)
        self.assertEqual(str(date_obj.end.time()), end)

    def test_error_if_end_before_start(self):

        start = "17:00:00"
        end = "09:01:02"

        with self.assertRaises(ValueError):
            TimeRange(start, end)

    def test_true_if_date_query_between_dates(self):

        start = "09:00:00"
        end = "17:01:02"

        date_obj = TimeRange(start, end)

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
