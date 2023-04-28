from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract class for commands"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.prefix = "!"

    @abstractmethod
    def execute(self, *args):
        ...
