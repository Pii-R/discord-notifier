"""Databases tests"""

from sqlalchemy import create_engine

from src.database.configuration import DatabaseConfiguration
from src.database.models import DiscordUser, Notifications, UserSettings


def test_create_discord_user(shared_datadir):
    """Test of correct creation of a user"""

    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    conf = DatabaseConfiguration(test_engine)
    user = DiscordUser(discord_id=2312312, discord_name="pierre")
    carl = DiscordUser(discord_id=1, discord_name="carl")
    conf.session.add_all([user, carl])
    conf.session.commit()

    assert conf.session.query(DiscordUser).count() == 2

    setting = UserSettings(discord=user, schedule="0 8 * * *")
    setting1 = UserSettings(discord=carl, schedule="0 9 * * *")
    conf.session.add_all([setting, setting1])
    conf.session.commit()
    assert setting.discord.discord_id == user.discord_id
    assert setting1.discord.discord_id == carl.discord_id
    assert conf.session.query(UserSettings).count() == 2


def test_create_usersettings_and_notifications(shared_datadir):
    """Test of correct creation of a user"""

    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    conf = DatabaseConfiguration(test_engine)

    user = DiscordUser(discord_id=2312312, discord_name="pierre")
    carl = DiscordUser(discord_id=1, discord_name="carl")

    conf.session.add_all([user, carl])
    conf.session.commit()

    lol_notif = Notifications(
        id=1,
        description="lol notification",
    )
    setting = UserSettings(
        discord=user, schedule="0 8 * * *", notification_id=lol_notif.id
    )
    setting1 = UserSettings(discord=carl, schedule="0 9 * * *")
    conf.session.add_all([setting, setting1])
    conf.session.commit()
    assert (
        len(
            conf.session.query(UserSettings).filter_by(discord_id=user.discord_id).all()
        )
        == 1
    )
    conf.session.query(UserSettings).filter_by(discord_id=user.discord_id).all()[
        0
    ].notification_id == lol_notif.id
