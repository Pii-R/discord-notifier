"""Logic for sending notification to subsribers"""
import asyncio

from sqlalchemy.sql.expression import func, select

import discord

from ..database.models import Citations


async def send_personnalized_message(user_id: int, client: discord.Client):
    # Wait until the scheduled time
    session = client.commands_handler.db_handler.session
    import random

    rand = random.randrange(0, session.query(Citations).count())
    row = session.query(Citations)[rand]
    citation = row.text
    wait = 5
    if user_id == 354731036644737024:
        wait = 5

    while 1:
        user = await client.fetch_user(int(user_id))
        # Send the message to the user
        await user.send(f"Voici ta citation du jour:\n{citation}")
        print(f"sent to {user_id} ")
        await asyncio.sleep(wait)


async def prepare_task(users_id: list, client: discord.Client):
    tasks = []
    for user_id in users_id:
        tasks.append(send_personnalized_message(user_id, client))
    await asyncio.gather(*tasks)
