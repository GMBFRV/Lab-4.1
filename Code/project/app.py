import os
import uuid
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

# Початкові дані
users = {
    'user1': {'user_id': '1', 'user_name': 'John Doe'},
    'user2': {'user_id': '2', 'user_name': 'Alice Johnson'},
    'user3': {'user_id': '3', 'user_name': 'Mike Bernard'},
}

categories = {
    '1': {'category_id': '1', 'category_name': 'car'},
    '2': {'category_id': '2', 'category_name': 'phone'},
    '3': {'category_id': '3', 'category_name': 'watch'},
    '4': {'category_id': '4', 'category_name': 'Watches', 'visibility': 'public', 'owner_id': '2'},
    '5': {'category_id': '5', 'category_name': 'House', 'visibility': 'public', 'owner_id': '1'},
    '6': {'category_id': '6', 'category_name': 'Healthcare', 'visibility': 'private', 'owner_id': '3'},
}

records = {
    'Music': {'record_id': '1', 'user_id': '1', 'category_id': '1', 'creation_data': '23-11-23', 'cost': '1000$'},
    'Games': {'record_id': '2', 'user_id': '2', 'category_id': '2', 'creation_data': '24-11-23', 'cost': '2000$'},
    'Food': {'record_id': '3', 'user_id': '3', 'category_id': '3', 'creation_data': '23-11-23', 'cost': '3000$'},
}

class UserSchema(Schema):
    user_name = fields.String(required=True)
    user_id = fields.String(required=True)

class CategorySchema(Schema):
    category_id = fields.String(required=True)
    category_name = fields.String(required=True, validate=validate.Length(min=1))
    visibility = fields.String(validate=validate.OneOf(['public', 'private']))
    owner_id = fields.String()

class RecordSchema(Schema):
    record_id = fields.String(required=True)
    user_id = fields.String(required=True)
    category_id = fields.String(required=True)
    creation_data = fields.String(required=True)
    cost = fields.String(required=True)

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

@app.route('/')
def hello_world():
    return 'This is Lab-work #3'

# Вивід списку користувачів
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Вивід конкретного користувача по ID
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users.values() if user['user_id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Створення користувача
@app.route('/user', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    user_id = user_data.get('user_id')
    user = {'user_id': user_id, **user_data}
    users[user_id] = user
    return jsonify(user_schema.dump(user))

# Видалення користувача
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users.values() if user['user_id'] == user_id), None)
    if user:
        deleted_user = users.pop(user_id)
        return jsonify({'message': 'User deleted successfully', 'user': deleted_user})
    return jsonify({'error': 'User not found'}), 404

# Вивід списку категорій
@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(categories)

# Створення категорії
@app.route('/category', methods=['POST'])
def create_category():
    try:
        category_data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    category_id = category_data.get('category_id')
    category = {'category_id': category_id, **category_data}
    categories[category_id] = category
    return jsonify(category_schema.dump(category))

# Видалення категорії по ID
@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((category for category in categories.values() if category['category_id'] == category_id), None)
    if category:
        deleted_category = categories.pop(category_id)
        return jsonify({'message': 'Category deleted successfully', 'category': deleted_category})
    return jsonify({'error': 'Category not found'}), 404

# Створення запису
@app.route('/record', methods=['POST'])
def create_record():
    try:
        record_data = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    category_id = record_data['category_id']
    category = categories.get(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    visibility = category.get('visibility', 'public')
    # Перевірка видимості категорії
    if visibility == 'private':
        user_id = record_data['user_id']
        if user_id != category.get('owner_id'):
            return jsonify({'error': 'You are not allowed to use this category'}), 403

    record_id = record_data.get('record_id')
    record = {'record_id': record_id, **record_data}
    records[record_id] = record
    return jsonify(record_schema.dump(record))

# Вивід списку записів по певному користувачу та/або категорії
@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    if not user_id and not category_id:
        return jsonify({'error': 'At least one of user_id or category_id is required'}), 400

    filtered_records = [record for record in records.values() if
                        (not user_id or record['user_id'] == user_id) and
                        (not category_id or record['category_id'] == category_id)]
    return jsonify(filtered_records)

# Видалення запису
@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    for record_key, record in records.items():
        if record['record_id'] == record_id:
            deleted_record = records.pop(record_key)
            return jsonify({'message': 'record deleted successfully', 'deleted record': deleted_record})
    return jsonify({'error': 'Record not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
