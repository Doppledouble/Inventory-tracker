from enum import Enum


class TransactionType(str, Enum):
    ADD         = "add"
    ADJUSTMENT  = "adjustment"
    ASSIGNMENT  = "assignment"
    RETURN      = "return"
    REMOVE      = "remove"
    WITHDRAW    = "withdraw"
    
    
class ItemType(str, Enum):
    MATERIAL    = "material"
    TOOL        = "tool"