from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!")
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save()
            return item.json(), 201
        except:
            return {"message": "An error eccurred inserting the item."}

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message': "Item deleted."}
        else:
            return {'message': "Item does not exist."}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save()
        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items': list(map(lambda x: x.json(), items))}
