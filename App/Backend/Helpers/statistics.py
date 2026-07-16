from Backend.utils.constants import *
import json



def load_statistics():
    with open(STATISTICS_DB_PATH, "r") as f:
        return json.load(f)


def save_statistics(settings):
    with open(STATISTICS_DB_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def Levelup(user):
    with open(STATISTICS_DB_PATH, 'r') as f:
        statistics= json.load(f)
        while True:
            if statistics.experience >=100:
                statistics.experience -= 100
                statistics.Level+=1
                if statistics.Level <=5:
                    statistics.Title = LEVELNAME[statistics.Level]
            else: 
                return None