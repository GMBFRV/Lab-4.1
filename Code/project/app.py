import uuid

from flask import Flask, request, jsonify

app = Flask(__name__)

# Початкові дані
users = {
    'user1': {'user_id': '1', 'user_name': 'John Doe'},
    'user2': {'user_id': '2', 'user_name': 'Alice Johnson'},
    'user3': {'user_id': '3', 'user_name': 'Mike Bernard'}, }

categories = {
    'car': {'category_id': '1', 'category_name': 'car'},
    'phone': {'category_id': '2', 'category_name': 'phone'},
    'watch': {'category_id': '3', 'category_name': 'watch'}, }

records = {
    'Music': {'record_id': '1', 'user_id': '1', 'category_id': '1', 'creation_data': '23-11-23', 'cost': '1000$'},
    'Games': {'record_id': '2', 'user_id': '2', 'category_id': '2', 'creation_data': '24-11-23', 'cost': '2000$'},
    'Food': {'record_id': '3', 'user_id': '3', 'category_id': '3', 'creation_data': '23-11-23', 'cost': '3000$'}
}


@app.route('/')
def hello_world():
    return 'This is Lab-work #2'


#             #---------------------------------------------------------------------------------------------------------
# Користувачі #---------------------------------------------------------------------------------------------------------
#             #---------------------------------------------------------------------------------------------------------


# Вивід списку користувачів
@app.route('/users', methods=['GET'])
def get_users():
    return list(users.values())


# Вивід конкретного користувача по ID
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    for user_key, user in users.items():
        if user['user_id'] == user_id:
            return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


# Створення користувача
@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return user


# Видалення користувача
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user_key, user in users.items():
        if user['user_id'] == user_id:
            deleted_user = users.pop(user_key)
            return jsonify({'message': 'User deleted successfully', 'user': deleted_user})

    return jsonify({'error': 'User not found'}), 404


#            #----------------------------------------------------------------------------------------------------------
# Категорії  #----------------------------------------------------------------------------------------------------------
#            #----------------------------------------------------------------------------------------------------------


# Вивід списку категорій
@app.route('/category', methods=['GET'])
def get_categories():
    return list(categories)


# Створення категорії
@app.route('/category', methods=['POST'])
def create_category():
    category_data = request.get_json()
    category_name = category_data.get('category_name')
    if category_name is None:
        return jsonify({'error': 'Category name is required'}), 400
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    categories[category_name] = category
    return jsonify(category)


# Видалення категорії по ID
@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    for category_key, category in categories.items():
        if category['category_id'] == category_id:
            deleted_category = categories.pop(category_key)
            return jsonify({'message': 'Category deleted successfully', 'category': deleted_category})

    return jsonify({'error': 'Category not found'}), 404


#            #----------------------------------------------------------------------------------------------------------
# Записи     #----------------------------------------------------------------------------------------------------------
#            #----------------------------------------------------------------------------------------------------------


# Створення запису
@app.route('/record', methods=['POST'])
def create_record():
    record_data = request.get_json()
    record_name = record_data.get('record_id')
    if record_name is None:
        return jsonify({'error': 'Record ID is required'}), 400
    record_id = uuid.uuid4().hex
    record = {"id": record_id, **record_data}
    records[record_name] = record
    return jsonify(record)


# Вивід списку записів по певному користувачу та/або категорії
@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    if not user_id and not category_id:
        return jsonify({'error': 'At least one of user_id or category_id is required'}), 400
    filtered_records = [record for record_id, record in records.items() if
                        (not user_id or record['user_id'] == user_id) and
                        (not category_id or record['category_id'] == category_id)]
    return jsonify(filtered_records)


# Видалення запису
@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    for record_key, record in records.items():
        if record['record_id'] == record_id:
            deleted_record = records.pop(record_key)
            return jsonify({'message': 'record deleted successfully', 'category': deleted_record})
    return jsonify({'error': 'Record not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
