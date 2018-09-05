from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self,name):
		store =  StoreModel.find_item_by_name(name)
		if store:
			return store.json()
		else:
			return {"message":"store not found"}

	def post(self,name):
		if StoreModel.find_item_by_name(name):
			return {"message":"A store with name '{}' already exist".format(name)}
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			{"message":"error in creating the store"}

		return store.json()

	def delete(self,name):
		store = StoreModel.find_item_by_name(name)
		if store:
			store.delete_from_db()

		return {"message":"store deleted"}


class StoreList(Resource):
	def get(self):
		return {"stores":[store.json() for store in StoreModel.query.all()]}