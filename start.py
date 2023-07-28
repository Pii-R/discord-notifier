from src.discord.bot import DiscordSettings, DiscordBot

if __name__ == "__main__":
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    bot = DiscordBot(settings)
    bot.run()
