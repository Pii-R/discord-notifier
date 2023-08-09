"""Utils function for tasks"""

from datetime import datetime

import pytz
from croniter import croniter


def cron_to_datetime(cron_expression: str, timezone: str) -> datetime:
    """_summary_

    Args:
        cron_expression: cron time "0 8 * * *"

    Returns:
        the next occurence
    """
    # Get the current time as a datetime object
    local_now = datetime.now()
    # Create a croniter object based on the cron expression and the current time
    cron = croniter(cron_expression, local_now)
    # Calculate the next occurrence of the cron expression
    next_occurrence_local: datetime = cron.get_next(datetime)

    return pytz.timezone(timezone).localize(next_occurrence_local)


def get_sleep_time_until_next_occurence(cron: str, timezone: str) -> int:
    """get the amount of seconds to wait until the next occurence from a cron

    Args:
        next_occurence: next occurence

    Returns:
        totals seconds to wait
    """
    local_timezone = pytz.timezone(timezone)
    current_time = local_timezone.localize(datetime.now())
    target_time = cron_to_datetime(cron, timezone)
    print(current_time, target_time)
    # Calculate the time difference to the target time
    time_diff = (target_time - current_time).total_seconds()
    # If the target time has already passed, schedule the message for the next day
    if time_diff <= 0:
        target_time += datetime.timedelta(days=1)
        time_diff = (target_time - current_time).total_seconds()
    return time_diff
