from Backend.utils.constants import *
import json
def user_exists(username):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return True

    return False

def load_users():
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)
    
def valid_user(username, password):
    users=load_users()
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                return True
            else:
                return False
    return False

def register_user(username,password):

    with open(USER_DB_PATH, "r") as f:
        users = json.load(f)

        users.append({
            "username": username,
            "password": password
        })

    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=4)
