"""Tests of utils tasks function"""
from datetime import datetime, timedelta
from unittest.mock import patch

from src.tasks.utils import cron_to_datetime, get_sleep_time_until_next_occurence


def test_get_next_datetime_from_cron():
    """Check if the next date tis correct from a cron time"""
    next_cron = cron_to_datetime("0 8 * * *")

    assert next_cron == (datetime.now() + timedelta(days=1)).replace(
        second=0, minute=0, hour=8, microsecond=0
    )

    every_minute = cron_to_datetime("* * * * *")
    assert every_minute == (datetime.now() + timedelta(minutes=1)).replace(
        second=0, microsecond=0
    )


def test_get_sleeping_time_until_next_occurence_before_next():
    """test the right amount of time to wait until the next occurence"""
    current_datetime = datetime(2023, 1, 1, 8, 0, 0)

    class MockDatetime(datetime):
        def now():
            return current_datetime

    with patch("src.tasks.utils.datetime", MockDatetime):
        seconds_to_wait = get_sleep_time_until_next_occurence("0 20 * * *")
        assert (
            seconds_to_wait
            == (datetime(2023, 1, 1, 20, 0, 0) - current_datetime).seconds
        )


def test_get_sleeping_time_until_next_occurence_after_next():
    """test the right amount of time to wait until the next occurence"""
    current_datetime = datetime(2023, 1, 2, 8, 0, 0)

    class MockDatetime(datetime):
        def now():
            return current_datetime

    with patch("src.tasks.utils.datetime", MockDatetime):
        seconds_to_wait = get_sleep_time_until_next_occurence("0 20 * * *")
        assert (
            seconds_to_wait
            == (datetime(2023, 1, 2, 20, 0, 0) - current_datetime).seconds
        )
