import uuid

from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    'user1': {'user_id': '1', 'user_name': 'John Doe'},
    'user2': {'user_id': '2', 'user_name': 'Alice Johnson'},
    'user3': {'user_id': '3', 'user_name': 'Mike Bernard'}, }

categories = {
    'car': {'category_id': '1', 'category_name': 'car'},
    'phone': {'category_id': '2', 'category_name': 'phone'},
    'watch': {'category_id': '3', 'category_name': 'watch'}, }

records = {
    'record1': {'record_id': '1', 'user_id': '1', 'category_id': '1', 'creation_data': '23-11-23', 'cost': '1000$'},
    'record2': {'record_id': '2', 'user_id': '2', 'category_id': '2', 'creation_data': '24-11-23', 'cost': '2000$'},
    'record3': {'record_id': '3', 'user_id': '3', 'category_id': '3', 'creation_data': '23-11-23', 'cost': '3000$'}
}


@app.route('/')
def hello_world():  # put application's code here
    return 'This is Lab-work #2'


#            #----------------------------------------------------------------------------------------------------------
# Користувач #----------------------------------------------------------------------------------------------------------
#            #----------------------------------------------------------------------------------------------------------


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

# Вивід списку категорій
@app.route('/category', methods=['GET'])
def get_categories():
    return list(categories)


# Створення запису


if __name__ == '__main__':
    app.run()
