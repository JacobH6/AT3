import os
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
USER_DB_PATH = os.path.join(BASE_DIR, "Databases", "users.json")
SETTING_DB_PATH = os.path.join(BASE_DIR, "Databases", "settings.json")
STATISTICS_DB_PATH = os.path.join(BASE_DIR, "Databases", "statistics.json")

LEVELNAME = {
    0:"Rookie",
    1:"Trainee",
    2:"Gym-Smart",
    3:"Health-Nut",
    4:"Professional",
    5:"Trainer"

}