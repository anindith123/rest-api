from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price", type = float, required = True, help = "This field cannot be left empty!")
	
	parser.add_argument("store_id", type = int, required = True, help = "every item need store id")

	@jwt_required()
	

	def get(self,name):
		result = ItemModel.find_item_by_name(name)
		if result:
			return result.json()
		return {"message":"item does not exist"}

	def post(self,name):
		if ItemModel.find_item_by_name(name):
			return {'message' : "An item with name '{}' already exist".format(name)},400
		data = Item.parser.parse_args()
		item = ItemModel(name,data['price'],data['store_id'])

		try:
			item.save_to_db()
		except:
			return {"message":"error inserting the item"},500
		return item.json(),201


	def delete(self,name):
		item = ItemModel.find_item_by_name(name)
		if item:
			item.delete_from_db()

		return {'message':"Item deleted"}

	def put(self,name):
		data = Item.parser.parse_args()
		item =  ItemModel.find_item_by_name(name)
		
		if item is None:
			item = ItemModel(name, data['price'],data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items' : [item.json() for item in ItemModel.query.all()]}