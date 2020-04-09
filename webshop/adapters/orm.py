import typing
import collections
from uuid import UUID

import sqlalchemy
from sqlalchemy import Table, Column, String, Float, Integer, create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, Session, mapper
from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy_utils.functions import create_database, drop_database

from webshop.domain.ports import UnitOfWorkManager, UnitOfWork, ItemRepositorySpec
from webshop.domain.models import Item

SessionFactory = typing.Callable[[], sqlalchemy.orm.Session]

class ItemRepository(ItemRepositorySpec):
    def __init__(self, session):
        self.session = session

    def add(self, item: Item) -> UUID:
        self.session.add(item)
        return item.id

    def remove(self, item: Item):
        self.session.remove(self.item)


    def _get(self, item_id: UUID) -> Item:
        return self.session.query(Item) \
            .filter_by(id = item_id) \
            .first()

class SqlAlchemyUnitOfWorkManager(UnitOfWorkManager):

    def __init__(self, session_maker: SessionFactory):
        self.session_maker = session_maker

    def start(self):
        return SqlAlchemyUnitOfWork(self.session_maker)


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, sessionfactory: SessionFactory) -> None:
        self.sessionfactory = sessionfactory

    def __enter__(self):
        self.session = self.sessionfactory()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def commit(self):
        self.session.flush()
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def items(self):
        return ItemRepository(self.session)


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self._session_maker = scoped_session(sessionmaker(self.engine),)

    @property
    def unit_of_work_manager(self):
        return SqlAlchemyUnitOfWorkManager(self._session_maker)

    def register_in(self, container):
        container.register(SessionFactory, lambda x: self._session_maker)
        container.register(UnitOfWorkManager, SqlAlchemyUnitOfWorkManager)

    def recreate_schema(self):
        self.configure_mappings()
        drop_database(self.engine.url)
        self.create_schema()

    def create_schema(self):
        create_database(self.engine.url)
        self.metadata.create_all()

    def configure_mappings(self):
        self.metadata = MetaData(self.engine)
        items_table = Table('items',self.metadata,
                        Column('id', UUIDType, primary_key = True),    
                        Column('name', String(50)),
                        Column('description', String(100)),
                        Column('category', String(50)),
                        Column('price', Float),
                        Column('qty', Integer)
                    )

        mapper(Item, items_table, properties = {
            'id': items_table.c.id,
            'name': items_table.c.name,
            'description': items_table.c.description,
            'price': items_table.c.price,
            'category': items_table.c.category
        })


class SqlAlchemySessionContext:

    def __init__(self, session_maker):
        self._session_maker = session_maker

    def __enter__(self):
        self.session = self._session_maker()

    def __exit__(self, type, value, traceback):
        self._session_maker.remove()
