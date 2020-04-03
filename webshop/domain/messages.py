from typing import NamedTuple
import uuid

class AddItem(NamedTuple):
    name: str
    description: str
    price: float

class PurchaseItem(NamedTuple):
    code: UUID
    qty: float

class StockItem(NamedTuple):
    code: UUID
    qty: int

class GetSalesValue(NamedTuple):
    pass