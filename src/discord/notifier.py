"""Logic for sending notification to subsribers"""
import asyncio

import discord

from ..database.logic import DatabaseOperation


async def send_personnalized_message(
    message: str, user_id: int, client: discord.Client
):
    # Wait until the scheduled time

    wait = 5
    while 1:
        user = await client.fetch_user(int(user_id))
        # Send the message to the user
        await user.send(message)
        print(f"sent to {user_id}")
        await asyncio.sleep(wait)


def create_message_of_random_quote(db_handler: DatabaseOperation) -> str:
    """Create a message with a random quote from a database

    Args:
        db_handler: database handler where quotes are stored

    Returns:
        the formatted message with the quote
    """
    quote = db_handler.get_random_quote()
    return f"Your inspiring quote of the day:\n{quote}"


async def prepare_tasks(db_handler: DatabaseOperation, client: discord.Client):
    tasks = []
    users_id = db_handler.get_all_subscribed_user()
    for user_id in users_id:
        tasks.append(
            send_personnalized_message(
                create_message_of_random_quote(db_handler),
                user_id,
                client,
            )
        )
    return await asyncio.gather(*tasks)
