from app import app
from db import fb

db.init_app(app)

@app.before_first_request
def create_table():
	db.create_all()