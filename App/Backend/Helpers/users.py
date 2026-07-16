from Backend.utils.constants import *
import json
from werkzeug.security import generate_password_hash, check_password_hash
from random import *
    
def user_exists(username):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return True

    return False

def get_user_by_username(username):
    with open(USER_DB_PATH, "r") as f:
        users = json.load(f)

    for user in users:
        if user["username"] == username:
            return user
    
    return None
        
def get_user_settings(username):
    with open(SETTING_DB_PATH, "r") as f:
        settings = json.load(f)

    return settings.get(username, {})

def get_user_statistics(username):
    with open(STATISTICS_DB_PATH, "r") as f:
        statistics = json.load(f)

    return statistics.get(username, {})


def load_users():
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)
    
def valid_user(username, password):
    users=load_users()
    for user in users:
        if user["username"] == username:
            if check_password_hash(user["password"], password) :
                return True
            else:
                return False
    return False

def generate_user_id():
    users = load_users()
    generated_id=randint(0,100000000000)
    generating=True
    while generating:
        for user in users:
            if user["user_ID"] == generated_id:
                generated_id=randint(0,100000000000)
                continue
        generating=False
    return generated_id

def register_user(username,password):

    with open(USER_DB_PATH, "r") as f:
        users = json.load(f)

        users.append({
            "username": username,
            "password": generate_password_hash(password),
            "user_ID": generate_user_id()
        })

    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=4)



    with open(STATISTICS_DB_PATH, 'r') as f:
        statistics= json.load(f)

        statistics[username]={
            "Level": 0,
            "Title": "Rookie",
            "experience":0,
            "excercise_history":{}
        }
    with open(STATISTICS_DB_PATH, "w") as f:
        json.dump(statistics, f, indent=4)
    

    with open(SETTING_DB_PATH, "r") as f:
        settings = json.load(f)

        settings[username]={
            "Dark_mode": False,
        }

    with open(SETTING_DB_PATH, "w") as f:
        json.dump(settings, f, indent=4)
