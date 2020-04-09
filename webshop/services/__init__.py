import typing
import abc

from webshop.domain.messages import AddItem, PurchaseItem, StockItem
from webshop.domain.ports import UnitOfWorkManager, UnitOfWork
from webshop.domain.models import Item, ItemCategory, Shop

TMsg = typing.TypeVar('TMsg')

class Handles(typing.Generic[TMsg]):

    @abc.abstractmethod
    def handle(self, msg: TMsg):
        pass


class AddItemHandler(Handles[AddItem]):

    def __init__(self, uowm: UnitOfWorkManager):
        self.uowm = uowm

    def handle(self, cmd):
        item = Item(cmd.code, cmd.name, cmd.description, cmd.price, cmd.category)
        with self.uowm.start() as tx:
            tx.items.add(item)
            tx.commit()
        