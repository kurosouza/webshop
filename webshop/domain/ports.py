import abc
from uuid import UUID
from .models import Item, ItemNotFoundException

class ItemRepositorySpec(abc.ABC):

    @abc.abstractmethod
    def add(self, item: Item) -> UUID:
        pass

    @abc.abstractmethod
    def remove(self, item: Item):
        pass

    @abc.abstractmethod
    def _get(self, code: UUID) -> Item:
        pass

    def get(self, code: UUID) -> Item:
        item = self._get(code)
        if item is None:
            raise ItemNotFoundException()
        return item


class UnitOfWork(abc.ABC):

    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    @property
    @abc.abstractmethod    
    def items(self):
        pass


class UnitOfWorkManager(abc.ABC):

    @abc.abstractmethod
    def start(self) -> UnitOfWork:
        pass