from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "hjguigkgkuglg"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)



data = {1: {"name": "item1",
            "description": "This is item 1"},
        2: {"name": "item2",
            "description": "This is item 2"}
        }

users = {"admin": "password123"}
class Item (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}')"






@app.route('/')
def home():
    return "Hello world"


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{ item.id: {'name': item.name, 'description': item.description}} for item in items]), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item == None:
        return jsonify({"message": "Item not found"}), 404

    return jsonify([{ item.id: {'name': item.name, 'description': item.description}}]) , 200







#     item = data.get(item_id)
#     if item:
#         return jsonify(item)
#
#     return jsonify({"message": "Item not found"}), 404
#
#
#
@app.route('/items', methods=['POST'])
def create_item():
    json_data = request.get_json()  # Get data sent in the request body

    # Validate data (basic example)
    if not json_data or 'name' not in json_data or 'description' not in json_data:
        return jsonify({'message': 'Missing name or description'}), 400

    # Check for existing item
    if Item.query.filter_by(name=json_data['name']).first():
        return jsonify({'message': 'Item already exists'}), 409

    # Create new Item object
    new_item = Item(name=json_data['name'], description=json_data['description'])

    # Add to database session and commit
    db.session.add(new_item)
    db.session.commit()

    # Return success response
    return jsonify({'message': 'Item created', 'name': new_item.name, 'description': new_item.description}), 201
#
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No data provided"}), 400

    # Fetch the item from the database
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"message": "Item not found"}), 404

    # Update item properties if provided in json_data
    if 'name' in json_data:
        # Check if new name already exists in other items
        if Item.query.filter(Item.id != item_id, Item.name == json_data['name']).first():
            return jsonify({'message': 'Name already exists'}), 409
        item.name = json_data['name']

    if 'description' in json_data:
        # Optionally, ensure the description does not conflict
        if Item.query.filter(Item.id != item_id, Item.description == json_data['description']).first():
            return jsonify({'message': 'Description already exists'}), 409
        item.description = json_data['description']

    # Commit changes to the database
    db.session.commit()

    # Return a success response
    return jsonify({"message": "Item updated", "item": {"id": item.id, "name": item.name, "description": item.description}}), 200
#
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item has been deleted"}), 200










with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)






