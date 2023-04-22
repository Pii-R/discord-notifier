import asyncio
import os
import sqlite3
from datetime import datetime, timedelta

import dotenv

import discord
from discord.ext import commands

dotenv.load_dotenv(".env.test")
# Define the bot prefix
bot_prefix = "!"

# Define the bot token and client
bot_token = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.default())


# Connect to the SQLite database
conn = sqlite3.connect("user_settings.db")
c = conn.cursor()

# Create the user_settings table if it doesn't exist
c.execute(
    """
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id TEXT PRIMARY KEY,
        message_time TEXT
    )
"""
)


# Function to add or update user settings
def update_settings(user_id, time):
    c.execute(
        """
        INSERT OR REPLACE INTO user_settings
        VALUES (?, ?)
    """,
        (str(user_id), time),
    )
    conn.commit()


# Function to get user settings
def get_settings(user_id):
    c.execute(
        """
        SELECT message_time
        FROM user_settings
        WHERE user_id = ?
    """,
        (str(user_id),),
    )
    return c.fetchone()


# Function to get user settings
def get_id():
    c.execute(
        """
        SELECT user_id
        FROM user_settings
    """
    )
    return c.fetchall()


# Function to send a message at a specific time
async def send_timed_message(user_id, message):
    while True:
        # Get the user's settings
        settings = get_settings(user_id)
        # Check if the user has any settings
        if settings:
            # Get the current time and the scheduled time
            now = datetime.now()
            scheduled_time = datetime.strptime(settings[0], "%H:%M").replace(
                day=now.day, month=now.month, year=now.year
            )
            # Calculate the time until the scheduled time
            time_until = (scheduled_time - now).total_seconds()
            print(user_id, time_until)

            # Check if the scheduled time is in the future
            if time_until > 0:
                # Wait until the scheduled time
                await asyncio.sleep(time_until)
                user = await client.fetch_user(int(user_id))
                # Send the message to the user
                await user.send(message)

        # Wait for 1 minute before checking again
        await asyncio.sleep(2)


# Event to handle DM commands
@client.event
async def on_message(message):
    # Check if the message was sent in a DM channel and not by the bot itself
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        # Split the message into command and arguments
        command, *args = message.content.split()
        if command == bot_prefix + "settask":
            client.loop.create_task(task4())

        # Check if the message is a command
        if command == bot_prefix + "settime":
            # Check if the user provided a valid time
            try:
                # Parse the time from the argument
                time = datetime.strptime(args[0], "%H:%M").strftime("%H:%M")

                # Update the user's settings
                update_settings(message.author.id, time)

                # Send a confirmation message to the user
                await message.channel.send(
                    f"Your message schedule has been set to {time}."
                )
                # Start a background task to send the message

            except (ValueError, IndexError):
                # Send an error message to the user
                await message.channel.send(
                    "Please provide a valid time in the format HH:MM."
                )
        else:
            # Send an error message to the user
            await message.channel.send(
                "Sorry, I didn't understand that command. Please use '!settime HH:MM' to set your message schedule."
            )


async def task4():
    while True:
        print("Task 4")
        await asyncio.sleep(4)


async def main():
    tasks = []
    for user_id in get_id():
        tasks.append(send_timed_message(user_id[0], "This is your scheduled message!"))
    await asyncio.gather(*tasks)


@client.event
async def on_ready():
    client.loop.create_task(main())


client.run(bot_token)
