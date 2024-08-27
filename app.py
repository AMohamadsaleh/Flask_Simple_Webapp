from flask import Flask, request, jsonify


app = Flask(__name__)

app.secret_key = "hjguigkgkuglg"

data = {1: {"name": "item1",
            "description": "This is item 1"},
        2: {"name": "item2",
            "description": "This is item 2"}
        }

users = {"admin": "password123"}



@app.route('/')
def home():
    return "Hello world"


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)

    return jsonify({"message": "Item not found"}), 404



@app.route('/items', methods=['POST'])
def create_item():
    item_id = len(data) + 1
    name = request.json.get('name')
    description = request.json.get('description')
    data[item_id] = {"name": name, "description": description}

    return jsonify({"message": "Item is created", "item": data[item_id]}), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id in data:
        name = request.json.get('name')
        description = request.json.get('description')
        data[item_id] = {"name": name, "description": description}
        return jsonify({"message": "Item is updated", "item": data[item_id]})
    return jsonify({"message": "Item not found"}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data:
        deleted_item = data.pop(item_id)
        return jsonify({"message": "Item deleted", "item": deleted_item})
    return jsonify({"message": "Item not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)




