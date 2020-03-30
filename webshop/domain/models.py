import collections
import enum
from uuid import uuid4
from typing import DefaultDict, NamedTuple

class Item(object):

    def __init__(self, id: uuid4, name: str, description: str, price: float):
        self.id = uuid4
        self.name = name
        self.description = description
        self.price = price

    def __eq__(self, value):
        if value is not Item:
            return False
        if self.id == value.id:
            return True
        return False        
        

class Shop(object):

    def __init__(self):
        self.items = DefaultDict[Item, int]
        self.cash: float = 0.0

    def stockItem(self, item: Item, qty: int):
        if item in self.items:
            self.items[item] += qty
        else:
            self.items[item] = qty

    def sellItem(self, item: Item, qty: int):
        pass

    def updatePrice(self, item: Item, price: float):
        pass

    @property
    def cashInStore(self):
        raise NotImplementedError()


class ItemCategory(enum.Enum):
    Grocery = 0
    Toileteries = 1
    Beverages = 2
    Hardware = 3
    HomeEquipment = 4