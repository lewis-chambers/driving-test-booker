from src.my_logger import Logger
import os
import undetected_chromedriver
from datetime import datetime
from typing import Union, List


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

    def __init__(self, start: str, end: str, format: str = "%d/%m/%Y %H:%M:%S"):
        """Initialises the object.

        Args:
            start: Start time.
            end: End time.
            format: `datetime` format used.

        Returns:
            None.
        """
        self.start = datetime.strptime(start, format)
        self.end = datetime.strptime(end, format)

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

    def __init__(self, start: str, end: str, format: str = "%H:%M:%S"):
        """Initialises the object.

        Args:
            start: Start time.
            end: End time.
            format: `datetime` format used.

        Returns:
            None.
        """
        self.start = datetime.strptime(start, format)
        self.end = datetime.strptime(end, format)

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


# class WeekTimes:
#     """Represents the available times during each week."""

#     def __init__(self, )
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
