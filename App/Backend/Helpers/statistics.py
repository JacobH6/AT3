from Backend.utils.constants import *
from datetime import datetime
from markupsafe import escape
import json
import uuid



def load_statistics():
    with open(STATISTICS_DB_PATH, "r") as f:
        return json.load(f)


def save_statistics(settings):
    with open(STATISTICS_DB_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def Levelup(username):
    statistics=load_statistics()
    while True:
        if statistics[username]['experience'] >=100:
            statistics[username]['experience'] -= 100
            statistics[username]['Level']+=1
            if statistics[username]['Level'] <=5:
                statistics[username]['Title'] = LEVELNAME[statistics[username]['Level']]
        else: 
            save_statistics(statistics)
            return None
            
def generate_user_statistics(username):
    statistics = load_statistics()

    statistics[username]={
        "Level": 0,
        "Title": "Rookie",
        "experience":0,
        "Workouts":[],
        "days_experience":0
    }
    save_statistics(statistics)

def record_workout(username, workout):

    statistics = load_statistics()

    if username not in statistics:
        return False

    if "Workouts" not in statistics[username]:
        statistics[username]["Workouts"] = []

    # Validate and clean exercise name
    if "exercise" not in workout:
        return False
    workout["id"] = str(uuid.uuid4())
    workout["exercise"] = str(escape(workout["exercise"]))
    workout["exercise"] = workout["exercise"].strip().title()

    if len(workout["exercise"]) > 50:
        return False


    # Validate numeric fields
    try:
        if "weight" in workout:
            workout["weight"] = float(workout["weight"])

        if "reps" in workout:
            workout["reps"] = int(workout["reps"])

    except (ValueError, TypeError):
        return False


    if workout.get("weight", 0) < 0:
        return False

    if workout.get("reps", 0) < 0:
        return False


    # Add server-controlled data
    workout["timestamp"] = datetime.now().isoformat()
    workout["xp_gained"] = calcxp(workout["reps"],workout['weight'])


    statistics[username]["Workouts"].append(workout)
    save_statistics(statistics)

    giveXp(username,workout["reps"],workout['weight'])
    Levelup(username)

    return True
def calcxp(reps,weight):
    return int((reps*weight)//12)

def giveXp(username,reps,ammount):
    statistics = load_statistics()
    statistics[username]['experience']+=int((reps*ammount)//12)
    save_statistics(statistics)
    return True
