from ..orm import SqlAlchemy
from webshop.services import AddItemHandler

import webshop.domain.messages as msgs

db = SqlAlchemy('sqlite:///webshop.db')
db.configure_mappings()
db.create_schema()

add_item = AddItemHandler(db.unit_of_work_manager)