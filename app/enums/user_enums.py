from enum import Enum

class Roles(Enum):
    USER = "user"

    def __str__(self):
        return self.value