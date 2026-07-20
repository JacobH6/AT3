from flask import Flask, render_template, session, request, redirect, url_for, g
import json
import os
from Backend.Helpers.users import *
from Backend.Helpers.settings import *
from Backend.Helpers.statistics import *
from Backend.utils.constants import *
import secrets
from markupsafe import escape
from datetime import datetime
from flask import send_from_directory
from Backend.Helpers.ai import ask_ai
app = Flask(
    __name__,
    template_folder="../Frontend/templates",
    static_folder="../Frontend/static"

)
app.secret_key = "9906b46b294f624da5f0ebdf88476f9bcc54511749683331845bdd6d6edd0ef9"
@app.before_request
def require_login():
    allowed_paths = ["/", "/register"]

    if request.path in allowed_paths:
        if "user" in session:
            return redirect(url_for("main"))
        return  # allow login page

    if request.path.startswith("/static/"):
            return

    if "user" not in session:
        return redirect(url_for("login"))
    
@app.before_request
def load_user():
    username = session.get("user")

    if username:
        g.user = get_user_by_username(username)
        g.settings = get_user_settings(username)
        g.statistics = get_user_statistics(username)


        today = datetime.now().date()

        g.statistics["days_experience"] = sum(
            workout.get("xp_gained", 0)
            for workout in g.statistics.get("Workouts", [])
            if datetime.fromisoformat(
                workout["timestamp"]
            ).date() == today
        )

    else:
        g.user = None
        g.settings = None
        g.statistics = None


@app.context_processor
def inject_user():
    return {
        "user": g.user,
        "settings": g.settings,
        "statistics":g.statistics
    }












@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST request
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html",error="Username or Password cannot be empty fields")

    if valid_user(username, password):
        session["user"] = username
        return redirect(url_for("main"))

    return render_template(
        "login.html",
        error="Invalid username or password"
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        return render_template("register.html",error="Username or Password cannot be empty fields")

    if user_exists(username):
        return render_template("register.html",error="Account name already in use")
    
    if not validate_registration(username):
        return render_template("register.html",error="Username Must be between 3 and 13 charecters and must only contain alphanumeric charecters and underscores")

    register_user(username,password)
    session["user"] = username
    return redirect(url_for("main"))

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/graphs")
def graphs():
    return render_template("graphs.html")

@app.route("/scores")
def scores():
    return render_template("scores.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.post("/api/settings/darkmode")
def toggle_darkmode():
    username = session["user"]
    if not username:
            return {"error": "Not logged in"}, 401

    settings = load_settings()

    if username not in settings:
        return {"error": "User settings not found"}, 404

    settings[username]["Dark_mode"] = not settings[username].get(
        "Dark_mode",
        False
    )

    save_settings(settings)

    return {
        "dark_mode": settings[username]["Dark_mode"]
    }

@app.get("/api/leaderboard")
def leaderboard():

    statistics = load_statistics()

    rankings = []

    for username, stats in statistics.items():
        rankings.append({
            "username": username,
            "level": stats["Level"],
            "experience": stats["experience"]
        })

    rankings.sort(
        key=lambda player: (
            player["level"],
            player["experience"]
        ),
        reverse=True
    )
    return {
        "leaderboard": rankings[:10]
    }

@app.post("/api/workouts")
def add_workout():
    data = request.get_json()

    if not data:
        return {"error": "Invalid request"}, 400


    exercise = data["exercise"]
    try:
        weight = float(data["weight"])
        reps = int(data["reps"])
    except (ValueError, TypeError):
        return {"error": "Invalid values"}, 400

    if weight < 0 or reps < 0:
        return {"error": "Values cannot be negative"}, 400



    record_workout(g.user["username"],data)
    statistics = get_user_statistics(g.user['username'])

    return {
        "success": True,
        "level": statistics["Level"],
        "experience": statistics["experience"],
        "title": statistics["Title"]
    }


@app.get("/api/xp-history")
def xp_history():

    statistics = get_user_statistics(session["user"])

    daily_xp = {}

    for workout in statistics["Workouts"]:

        date = datetime.fromisoformat(
            workout["timestamp"]
        ).date().isoformat()

        exercise = workout["exercise"]
        xp = workout.get("xp_gained", 0)


        if date not in daily_xp:
            daily_xp[date] = {}


        if exercise not in daily_xp[date]:
            daily_xp[date][exercise] = 0


        daily_xp[date][exercise] += xp


    return {
        "history": daily_xp
    }

@app.get("/api/workouts")
def get_workouts():

    stats = get_user_statistics(session["user"])

    stats["Workouts"].sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return {
        "workouts": stats["Workouts"]
    }

@app.put("/api/workouts/<workout_id>")
def edit_workout(workout_id):

    data = request.get_json()

    statistics = load_statistics()

    workouts = statistics[session["user"]]["Workouts"]


    for workout in workouts:

        if workout["id"] == workout_id:

            workout["exercise"] = data["exercise"]
            workout["weight"] = data["weight"]
            workout["reps"] = data["reps"]

            break


    save_statistics(statistics)


    return {
        "success": True
    }

@app.delete("/api/workouts/<workout_id>")
def delete_workout(workout_id):

    statistics = load_statistics()

    workouts = statistics[session["user"]]["Workouts"]

    statistics[session["user"]]["Workouts"] = [
        workout for workout in workouts
        if workout["id"] != workout_id
    ]

    save_statistics(statistics)

    return {
        "success": True
    }

@app.route("/sw.js")
def service_worker():
    return send_from_directory(
        app.static_folder,
        "sw.js",
        mimetype="application/javascript"
    )

@app.post("/api/coach")
def ai():

    statistics = get_user_statistics(
        session["user"]
    )

    print(statistics)

    question = request.json["question"]


    prompt = f"""
You are a workout assistant.

Rules:
- Give concise advice.
- Use the user's workout history.
- Do not invent completed workouts.
- Encourage safe progression.
- Explain reasoning.

User statistics:

{statistics}


User question:

{question}

Answer:
"""


    response = ask_ai(prompt)


    return {
        "response": response
    }

@app.get("/api/progress-prediction")
def progress_prediction():

    statistics = get_user_statistics(
        session["user"]
    )

    daily_xp = {}

    for workout in statistics["Workouts"]:

        date = datetime.fromisoformat(
            workout["timestamp"]
        ).date().isoformat()

        xp = workout.get(
            "xp_gained",
            0
        )

        daily_xp[date] = (
            daily_xp.get(date, 0)
            + xp
        )


    if len(daily_xp) == 0:
        return {
            "error": "Not enough workout data"
        }


    average_xp = (
        sum(daily_xp.values())
        /
        len(daily_xp)
    )


    current_xp = statistics["experience"]

    xp_needed = 100 - current_xp


    days_to_level = (
        xp_needed / average_xp
    )

    if average_xp > 500:
        advice = "Your progress is accelerating. Keep up the good work!"

    elif average_xp > 200:
        advice = "Your progress is steady. Not bad!"

    else:
        advice = "Try increasing workout consistency."


    return {

        "average_xp": round(
            average_xp,
            2
        ),

        "days_to_level": round(
            days_to_level,
            1
        ),
        "advice": advice

    }

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True,port=8000)