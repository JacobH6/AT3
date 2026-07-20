from Backend.utils.constants import *
import json

def load_settings():
    with open(SETTING_DB_PATH, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTING_DB_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def generate_user_settings(username):
        

    with open(SETTING_DB_PATH, "r") as f:
        settings = json.load(f)

        settings[username]={
            "Dark_mode": False,
        }

    with open(SETTING_DB_PATH, "w") as f:
        json.dump(settings, f, indent=4)
