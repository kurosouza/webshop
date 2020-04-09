import uuid
from flask import Flask, request, jsonify
from webshop.domain.messages import AddItem
from webshop.services import AddItemHandler
from webshop.adapters.orm import SqlAlchemyUnitOfWorkManager
from . import config

app = Flask('webshop')

# uowm = SqlAlchemyUnitOfWorkManager()

@app.route('/item', methods = ['POST'])
def create_item():
    item_id = uuid.uuid4()
    add_item_command = AddItem(code = item_id, **request.get_json())
    config.add_item.handle(add_item_command)
    # handler = AddItemHandler(uowm)
    # pass
    return jsonify(add_item_command), 201, { 'Location': f'/items/{item_id}' }