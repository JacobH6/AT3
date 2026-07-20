import json
import os
from Backend.Helpers.users import *
from Backend.utils.constants import *

def init_db():
    os.makedirs(os.path.dirname(USER_DB_PATH), exist_ok=True)

    if not os.path.exists(USER_DB_PATH) or os.path.getsize(USER_DB_PATH) == 0:
        with open(USER_DB_PATH, "w") as f:
            json.dump([], f)
    if not os.path.exists(SETTING_DB_PATH) or os.path.getsize(SETTING_DB_PATH) == 0:
        with open(SETTING_DB_PATH, "w") as f:
            json.dump({}, f)
    if not os.path.exists(STATISTICS_DB_PATH) or os.path.getsize(STATISTICS_DB_PATH) == 0:
        with open(STATISTICS_DB_PATH, "w") as f:
            json.dump({}, f)
init_db()