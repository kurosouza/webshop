import collections
import enum
from uuid import UUID
from typing import DefaultDict, NamedTuple, Dict

class ItemNotFoundException(Exception):
    pass

class InsufficientItemsInStockException(Exception):
    pass


class ItemCategory(enum.Enum):
    Grocery = 0
    Toileteries = 1
    Beverages = 2
    Hardware = 3
    HomeEquipment = 4

class Item(object):

    def __init__(self, id: UUID, name: str, description: str, price: float, category: ItemCategory = ItemCategory.Hardware):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def __eq__(self, value):
        if value is not Item:
            return False
        if self.id == value.id:
            return True
        return False

    def __hash__(self):
        return super().__hash__()

    @classmethod
    def from_dict(cls, props):
        item = Item(id = props['id'], name=props['name'], description=props['description'], price = props['price'])
        return item        
        

class Shop(object):
    ''' items: a collection containing the items available in the shop. Should be contained on an appropriate data structure
                Dict[id, NamedTuple] may work for now 

    '''
    @classmethod
    def create(cls, items: Dict[Item, int]):
        pass

    @classmethod
    def from_array(cls, items):
        shop = Shop()
        for i in items:
            item = Item.from_dict(i)            
            shop.stockItem(item, 1)
        return shop

    def __init__(self):
        self.items_qty = collections.defaultdict()
        self.items_info = collections.defaultdict(None)
        self.cash: float = 0.0
 
    def getItem(self, uid: UUID) -> Item:
        if uid not in self.items_info:
            raise ItemNotFoundException()
        return self.items_info[uid]

    def stockItem(self, item: Item, qty: int):
        if item.id in self.items_qty:
            self.items_qty[item.id] += qty            
        else:
            self.items_qty[item.id] = qty
            self.items_info[item.id] = item

    def sellItem(self, item: Item, qty: int):
        if item.id in self.items_qty:
            if self.items_qty[item.id] <= qty:
                self.items_qty[item.id] -= qty
                self.cash += self.items_info[item.id].price * qty
            else:
                raise InsufficientItemsInStockException()
        else:
            raise ItemNotFoundException()        

    def updatePrice(self, item: Item, price: float):
        pass

    def checkItemQty(self, item: Item) -> int:
        if item.id not in self.items_qty:
            raise ItemNotFoundException()
        else:
            return self.items_qty[item.id]
            
    @property
    def cashInStore(self):
        return self.cash