from src.notifier.handler import DiscordSettings, DiscordMessageHandler
from src.notifier.command import Help, Subscribe, Unsubscribe
from src.models.session import execute_engine

if __name__ == "__main__":
    execute_engine()
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    handler = DiscordMessageHandler(
        settings, commands=[Help, Subscribe, Unsubscribe], prefix="!"
    )
    handler.run()
