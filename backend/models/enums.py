from enum import Enum


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    ASSIGNMENT = "assignment"
    RETURN = "return"
    DAMAGE = "damage"
    ADJUSTMENT = "adjustment"