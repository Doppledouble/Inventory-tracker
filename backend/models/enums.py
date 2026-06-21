from enum import Enum


class TransactionType(str, Enum):
    ADD = "add"
    ASSIGNMENT = "assignment"
    RETURN = "return"
    REMOVE = "remove"
    ADJUSTMENT = "adjustment"