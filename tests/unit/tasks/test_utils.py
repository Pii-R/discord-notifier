"""Tests of utils tasks function"""
from datetime import datetime, timedelta
from unittest.mock import patch

import pytz

from src.tasks.utils import cron_to_datetime, get_sleep_time_until_next_occurence


def test_get_next_datetime_from_cron():
    """Check if the next date tis correct from a cron time"""
    next_cron = cron_to_datetime("0 8 * * *", timezone="UTC")

    assert next_cron == (datetime.now(tz=pytz.UTC) + timedelta(days=1)).replace(
        second=0, minute=0, hour=8, microsecond=0
    )

    every_minute = cron_to_datetime("* * * * *", timezone="UTC")
    assert every_minute == (datetime.now() + timedelta(minutes=1)).replace(
        second=0, microsecond=0, tzinfo=pytz.UTC
    )


def test_get_sleeping_time_until_next_occurence_before_next():
    """test the right amount of time to wait until the next occurence"""
    current_datetime = datetime(2023, 1, 1, 8, 0, 0)

    class MockDatetime(datetime):
        def now(tz=None):
            return current_datetime

    with patch("src.tasks.utils.datetime", MockDatetime):
        seconds_to_wait = get_sleep_time_until_next_occurence("0 20 * * *", "UTC")
        assert (
            seconds_to_wait
            == (datetime(2023, 1, 1, 20, 0, 0) - current_datetime).seconds
        )


def test_get_sleeping_time_until_next_occurence_after_next():
    """test the right amount of time to wait until the next occurence"""
    current_datetime = datetime(2023, 1, 2, 8, 0, 0)

    class MockDatetime(datetime):
        def now(tz=None):
            return current_datetime

    with patch("src.tasks.utils.datetime", MockDatetime):
        seconds_to_wait = get_sleep_time_until_next_occurence("0 20 * * *", "UTC")
        assert (
            seconds_to_wait
            == (datetime(2023, 1, 2, 20, 0, 0) - current_datetime).seconds
        )


def test_get_sleeping_time_until_next_occurence_after_next_pt_tz():
    """test the right amount of time to wait until the next occurence"""
    current_datetime = datetime(
        2023,
        1,
        2,
        8,
        0,
        0,
    )
    pacific = pytz.timezone("US/Pacific")

    class MockDatetime(datetime):
        def now(tz=None):
            return current_datetime

    with patch("src.tasks.utils.datetime", MockDatetime):
        seconds_to_wait = get_sleep_time_until_next_occurence(
            "0 20 * * *", "US/Pacific"
        )
        assert (
            seconds_to_wait
            == (
                datetime(2023, 1, 2, 20, 0, 0, tzinfo=pytz.timezone("US/Pacific"))
                - current_datetime.replace(tzinfo=pytz.timezone("US/Pacific"))
            ).seconds
        )
