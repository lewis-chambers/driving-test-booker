from src.my_logger import Logger
import os
import undetected_chromedriver
from datetime import datetime
from typing import Union, List, Tuple


class App:
    def __init__(self):
        """Initialises the searcher."""

        self.log_dir = os.path.join(os.path.dirname(__file__), "logs")
        self.logger = Logger(__name__)

        self.driver = self.get_driver()

    def get_driver(self):
        driver = undetected_chromedriver.Chrome()
        self.logger.info("Started new chromedriver.")
        return driver


class DateRange:
    """Represented a range of two increasing dates."""

    def __init__(self, date_range: Tuple[str], *, format: str = "%d/%m/%Y %H:%M:%S"):
        """Initialises the object.

        Args:
            date_range: The date range given as a tuple of strings.
            format: `datetime` format used.

        Returns:
            None.
        """
        if not hasattr(date_range, "__iter__"):
            raise TypeError("`time_range` must be an iterable object.")
        if not len(date_range) == 2:
            raise ValueError(f"`time_range` must have 2 items, not '{len(date_range)}'")

        self.start = datetime.strptime(date_range[0], format)
        self.end = datetime.strptime(date_range[1], format)

        if self.start > self.end:
            raise ValueError("Start date must be before end date.")

    def is_between(self, date: datetime) -> bool:
        """Checks if date is between start and end.

        Args:
            date: Query datetime.
        Returns:
            True or false.
        """

        if not isinstance(date, datetime):
            raise TypeError("`date` must be a `datetime` object.")

        if self.start <= date <= self.end:
            return True

        return False


class Date:
    """Represents a date."""

    def __init__(self, date_string: str, format: str = "%d/%m/%Y"):
        """Instantiates the class.

        Args:
            date_str: String of the date.
            format: Format of the date string

        Returns:
            None.
        """

        datetime_obj = datetime.strptime(date_string, format)
        datetime_obj = datetime_obj.replace(hour=0, minute=0, second=0, microsecond=0)

        self.date = datetime_obj


class TimeRange:
    """A Time Range."""

    def __init__(self, time_range: Tuple[str], *, format: str = "%H:%M:%S"):
        """Initialises the object.

        Args:
            time_range: The time range.
            format: `datetime` format used.

        Returns:
            None.
        """

        if not hasattr(time_range, "__iter__"):
            raise TypeError("`time_range` must be an iterable object.")
        if not len(time_range) == 2:
            raise ValueError(f"`time_range` must have 2 items, not '{len(time_range)}'")

        self.start = datetime.strptime(time_range[0], format)
        self.end = datetime.strptime(time_range[1], format)

        if self.start.time() > self.end.time():
            raise ValueError("Start date must be before end date.")

    def is_between(self, date: datetime) -> bool:
        """Checks if date is between start and end.

        Args:
            date: Query datetime.
        Returns:
            True or false.
        """

        if not isinstance(date, datetime):
            raise TypeError("`date` must be a `datetime` object.")

        if self.start.time() <= date.time() <= self.end.time():
            return True

        return False


class WeekTimes:
    """Represents the available times during each week."""

    def __init__(
        self,
        time_range: Tuple[str],
        *,
        format: str = "%H:%M:%S",
        weekdays: Tuple[Tuple[str], bool] = (True, True, True, True, True, True, True),
    ):
        """Instanitates the class.

        Args:
            time_range: The default time range.
            format: String of the time range format.
            weekdays: Tuple of time ranges for each workday. A value of `False` means skip this day, and `True` uses default."""

        if not hasattr(time_range, "__iter__"):
            raise TypeError("`time_range` must be an iterable object.")
        if not len(time_range) == 2:
            raise ValueError(f"`time_range` must have 2 items, not '{len(time_range)}'")

        if not hasattr(weekdays, "__iter__"):
            raise TypeError("`weekdays` must be an iterable object.")
        if not len(weekdays) == 7:
            raise ValueError(f"`weekdays` must have 7 items, not '{len(weekdays)}'")

        for i, item in enumerate(weekdays):
            if not isinstance(item, bool) and not hasattr(item, "__iter__"):
                raise TypeError(f"weekdays[{i}] is not a bool or iterable:\n'{item}'")
            if not isinstance(item, bool) and len(item) != 2:
                raise ValueError(
                    f"Each item of `weekdays` must have 2 items, not '{len(item)}'"
                )

        self.weekdays = tuple(
            [x if isinstance(x, bool) else TimeRange(x) for x in weekdays]
        )

        self.time_range = TimeRange(time_range, format=format)

    def is_valid_time(self, date: datetime) -> bool:
        """Checks if date is between start and end.

        Args:
            date: Query datetime.
        Returns:
            True or false.
        """

        day = self.weekdays[date.weekday()]

        if day is True:
            return self.time_range.is_between(date)
        elif day is False:
            return False
        else:
            return day.is_between(date)


class Search:
    """Class for holding search details for application."""

    def __init__(
        self,
        time_range: DateRange,
        excluded_dates: Union[Date, List[Date]] = [],
        excluded_date_ranges: Union[DateRange, List[DateRange]] = [],
    ):

        if not isinstance(time_range, DateRange):
            TypeError("`time_range` must be a DateRange.")

        if not hasattr(excluded_dates, "__iter__"):
            excluded_dates = [excluded_dates]
        if not all([isinstance(x, Date) for x in excluded_dates]):
            raise TypeError("All `excluded_dates` must be a `Date` object.")

        self.time_range = time_range
        self.excluded_dates = excluded_dates


def main():
    app = Date("01/02/2022")

    a = 1


if __name__ == "__main__":
    main()
