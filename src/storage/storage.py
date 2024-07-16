import json
import os

"""
It’s like a database that stores user data. If you want to use this project somewhere, I recommend to use Postgres and SqlAlchemy
"""


USERS_FILE = 'users.json'


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


user_storage = load_users()
