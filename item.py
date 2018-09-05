from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price", type = float, required = True, help = "This field cannot be left empty!")
	@jwt_required()
	

	def get(self,name):
		result = Item.find_item_by_name(name)
		if result:
			return result
		return {"message":"item does not exist"}


	@classmethod
	def find_item_by_name(cls,name):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		select_query = "SELECT * FROM items WHERE name = ?"
		result = cursor.execute(select_query, (name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {"items": { "name": row[0], "price" : row[1]}}


	def post(self,name):
		if Item.find_item_by_name(name):
			return {'message' : "An item with name '{}' already exist".format(name)},400
		data = Item.parser.parse_args()
		item = {'name': name,'price' : data['price']}

		try:
			Item.insert(item)
		except:
			return {"message":"error inserting the item"},500
		return item,201

	@classmethod
	def insert(cls,data):
		item = {'name': data['name'],'price' : data['price']}
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		insert_query = "INSERT INTO items VALUES(?,?)"
		cursor.execute(insert_query,(item['name'],item['price']))
		connection.commit()
		connection.close()



	def delete(self,name):
		if Item.find_item_by_name(name):
			connection = sqlite3.connect("data.db")
			cursor = connection.cursor()

			delete_query = "DELETE FROM items WHERE name = ?"
			cursor.execute(delete_query,(name,))
			connection.commit()
			connection.close()

			return {"message": "item deleted"}
		return{"message":"item does not exist"}

	def put(self,name):
		data = Item.parser.parse_args()
		item = {"name" : name, "price" : data["price"]}
		if Item.find_item_by_name(item["name"]):
			Item.update(item)
		else:
			Item.insert(item)
		return item


	@classmethod
	def update(cls,data):
		item = {'name': data['name'],'price' : data['price']}
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "UPDATE items SET price =? WHERE name = ?"
		cursor.execute(query,([item["price"],item["name"]]))
		connection.commit()
		connection.close()


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "SELECT * FROM items"
		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({'name':row[0],'price':row[1]})

		connection.close()

		return {'items' : items}