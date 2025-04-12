from enum import Enum

class Roles(Enum):
    ADMIN = "admin"
    USER = "user"

    def __str__(self):
        return self.value