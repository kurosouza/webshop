test:
	PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 pytest -v

run:
	FLASK_APP=webshop.adapters.http.endpoints.py FLASK_ENV=development pipenv run flask run
	
send-create-item:
	http POST http://localhost:5000/item name='cookie' description='biscuit' category='edible' price=25