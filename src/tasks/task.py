import hashlib
from abc import ABC, abstractmethod


class Task(ABC):
    """Abstract class for tasks"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise Exception(f"{cls.__name__} can only be instantiated once.")
        cls._instance = super(Task, cls).__new__(cls)
        return cls._instance

    def __init_subclass__(cls, **kwargs):
        class_name = cls.__name__
        cls.id = int(hashlib.sha256(class_name.encode()).hexdigest(), 16)
        super().__init_subclass__(**kwargs)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
