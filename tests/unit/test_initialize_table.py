"""Tests of initialization of table"""

from sqlalchemy import Column, Integer, String, inspect

from src.database.base import Base
from src.database.configuration import DatabaseConfiguration, create_engine


def test_initialization(shared_datadir):
    """Test of initialization of the table"""
    test_engine = create_engine(f"sqlite:///{shared_datadir}/discord_bot_test.sqlite")

    class TestTable(Base):
        __tablename__ = "tabletest"
        id = Column(Integer, primary_key=True, autoincrement=True)
        discord_name = Column(String)
        summoner_name = Column(String, nullable=True)

    db_conf = DatabaseConfiguration(engine=test_engine)

    inspector = inspect(test_engine)
    table_names = inspector.get_table_names()
    assert TestTable.__tablename__ in table_names
    content = [
        {"discord_name": "pierre", "summoner_name": "pierrelol"},
        {"discord_name": "marc", "summoner_name": "marclol"},
    ]

    db_conf.initialize_table(TestTable, content)

    table = db_conf.session.query(TestTable).all()
    assert len(table) == len(content)
