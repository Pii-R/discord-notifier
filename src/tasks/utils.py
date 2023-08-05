"""Utils function for tasks"""

from datetime import datetime

from croniter import croniter


def cron_to_datetime(cron_expression: str) -> datetime:
    """_summary_

    Args:
        cron_expression: cron time "0 8 * * *"

    Returns:
        the next occurence
    """
    # Get the current time as a datetime object
    now = datetime.now()
    # Create a croniter object based on the cron expression and the current time
    cron = croniter(cron_expression, now)
    # Calculate the next occurrence of the cron expression
    next_occurrence = cron.get_next(datetime)

    return next_occurrence


def get_sleep_time_until_next_occurence(cron: str) -> int:
    """get the amount of seconds to wait until the next occurence from a cron

    Args:
        next_occurence: next occurence

    Returns:
        totals seconds to wait
    """
    current_time = datetime.now()
    target_time = cron_to_datetime(cron)
    # Calculate the time difference to the target time
    time_diff = (target_time - current_time).total_seconds()
    # If the target time has already passed, schedule the message for the next day
    if time_diff <= 0:
        target_time += datetime.timedelta(days=1)
        time_diff = (target_time - current_time).total_seconds()
    return time_diff
