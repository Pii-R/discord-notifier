"""Logic for sending notification to subsribers"""
import asyncio

import discord


async def send_personnalized_message(user_id: int, client: discord.Client):
    # Wait until the scheduled time
    wait = 2
    if user_id == 354731036644737024:
        wait = 5

    while 1:
        user = await client.fetch_user(int(user_id))
        # Send the message to the user
        await user.send("message stylé")
        print(f"sent to {user_id} ")
        await asyncio.sleep(wait)


async def prepare_task(users_id: list, client: discord.Client):
    tasks = []
    for user_id in users_id:
        tasks.append(send_personnalized_message(user_id, client))
    await asyncio.gather(*tasks)
