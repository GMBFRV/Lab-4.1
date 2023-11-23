import uuid
from flask import Flask, request

app = Flask(__name__)

users = {
    'user1': {'id': '1', 'name': 'John Doe'},
    'user2': {'id': '2', 'name': 'Alice Johnson'},
    'user3': {'id': '3', 'name': 'Mike Bernard'},
}

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return user

@app.route('/users', methods=['GET'])
def get_users():
    return list(users.values())


if __name__ == '__main__':
    app.run()

