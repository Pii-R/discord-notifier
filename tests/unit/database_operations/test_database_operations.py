"""Tests of operations on database"""
from sqlalchemy import create_engine

from src.database.configuration import DatabaseConfiguration
from src.database.logic import DatabaseOperation
from src.database.models import DiscordUser, Notifications, UserSettings


def test_get_all_subscribed_users(shared_datadir):
    """Check if all users are retrieved"""
    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    conf = DatabaseConfiguration(test_engine)
    user = DiscordUser(discord_id=2312312, discord_name="pierre")
    carl = DiscordUser(discord_id=1, discord_name="carl")
    conf.session.add_all([user, carl])
    conf.session.commit()

    assert conf.session.query(DiscordUser).count() == 2

    db_handler = DatabaseOperation(conf)

    assert sorted(db_handler.get_all_subscribed_user()) == sorted(
        [user.discord_id, carl.discord_id]
    )


def test_set_schedule(shared_datadir):
    """test of setting schedule for user and notification id"""
    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    conf = DatabaseConfiguration(test_engine)
    user = DiscordUser(discord_id=2312312, discord_name="pierre")
    carbonara = DiscordUser(discord_id=1, discord_name="carl")
    conf.session.add_all([user, carbonara])
    conf.session.commit()

    assert conf.session.query(DiscordUser).count() == 2

    db_handler = DatabaseOperation(conf)
    assert db_handler.set_notification_time(user.discord_id, "0 21 * * *", 1)
    assert not db_handler.set_notification_time(user.discord_id, "0 21 * * *", 1)


def test_link_between_user_settings_and_notifications(shared_datadir):
    """test"""
    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    conf = DatabaseConfiguration(test_engine)
    user = DiscordUser(discord_id=2312312, discord_name="pierre")
    carbonara = DiscordUser(discord_id=1, discord_name="carl")
    conf.session.add_all([user, carbonara])
    conf.session.commit()

    assert conf.session.query(DiscordUser).count() == 2

    db_handler = DatabaseOperation(conf)
    db_handler.set_notification_time(user.discord_id, "0 21 * * *", 1)
    user_settings = conf.session.query(UserSettings).all()
    print(user_settings[0])
