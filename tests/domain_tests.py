import uuid
from webshop.domain.models import Item, Shop

stockedItems = [
        {
            'id': uuid.uuid4(),
            'name': 'Large Towel',
            'description': 'Large Towel',
            'price': 5.0
        },
        {
            'id': uuid.uuid4(),
            'name': 'Salted Biscuits',
            'description': 'Salted Biscuits',
            'price': 2.0
        },
        {
            'id': uuid.uuid4(),
            'name': 'Electronic Calculator',
            'description': 'Electronic Calculator',
            'price': 5.0
        }
    ]

def test_shop_stock_item():
    shop = Shop.from_array(stockedItems)
    item = Item.from_dict(stockedItems[0])
    shop.stockItem(item, 2)
    assert shop.checkItemQty(item) == 3

def test_shop_sell_item():
    shop = Shop.from_array(stockedItems)
    item = Item.from_dict(stockedItems[0])
    shop.sellItem(item, 1)
    assert shop.items_qty[item.id] == 0
    assert shop.cash == stockedItems[0]['price']

def test_check_item_qty():
    shop = Shop.from_array(stockedItems)
    item = Item.from_dict(stockedItems[0])
    shop.stockItem(item, 1)
    assert shop.checkItemQty(item) == 2

def test_shop_from_dict():
    ''' Initialize a dictionary of items '''
    
    shop = Shop.from_array(stockedItems)
    # dir(shop.items.keys())
    assert stockedItems[0]['id'] in shop.items_qty


def test_item_from_dict():
    props = {
        'id': uuid.uuid4(),
        'name': 'Nike slippers',
        'description': 'Nike slippers',
        'price': 4.0
    }

    slipperItem = Item.from_dict(props)
    assert slipperItem.name == props['name']
    assert slipperItem.price == props['price']
    assert slipperItem.description == props['description']
    assert slipperItem.id == props['id']

def test_get_item():
    shop = Shop.from_array(stockedItems)
    assert shop.getItem(stockedItems[0]['id']).id == stockedItems[0]['id']