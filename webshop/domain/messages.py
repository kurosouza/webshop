from typing import NamedTuple
import uuid

class AddItem(NamedTuple):
    code: uuid.UUID
    name: str
    description: str
    price: float
    category: str

class PurchaseItem(NamedTuple):
    code: uuid.UUID
    qty: float

class StockItem(NamedTuple):
    code: uuid.UUID
    qty: int

class GetSalesValue(NamedTuple):
    pass