from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class DiscordUser(Base):
    __tablename__ = "discord_user"

    discord_id = Column(Integer, primary_key=True, autoincrement=False)
    discord_name = Column(String)
    summoner_name = Column(String, nullable=True)


if __name__ == "__main__":
    engine = create_engine("sqlite:///discord_bot.sqlite")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    user = DiscordUser(discord_id=1321321, discord_name="pierre")
    session.add(user)
    session.commit()
