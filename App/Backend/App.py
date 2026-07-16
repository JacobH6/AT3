from flask import Flask, render_template, session, request, redirect, url_for, g
import json
import os
from Backend.Helpers.users import *
from Backend.Helpers.settings import *
from Backend.Helpers.statistics import *
from Backend.utils.constants import *

app = Flask(
    __name__,
    template_folder="../Frontend/templates",
    static_folder="../Frontend/static"

)
app.secret_key = "You_Should_kill_yourself_NOW"
@app.before_request
def require_login():
    allowed_paths = ["/", "/register"]

    if request.path in allowed_paths:
        if "user" in session:
            return redirect(url_for("main"))
        return  # allow login page

    if "user" not in session:
        return redirect(url_for("login"))
    
@app.before_request
def load_user():
    username = session.get("user")

    if username:
        g.user = get_user_by_username(username)
        g.settings = get_user_settings(username)
        g.statistics = get_user_statistics(username)
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
        return render_template("register.html",error="Username or Password cannot be empty fields")

    if valid_user(username, password):
        session["user"] = username
        return redirect("/main")

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

    settings = load_settings()

    settings[username]["dark_mode"] = not settings[username].get("dark_mode", False)

    save_settings(settings)

    return {
        "dark_mode": settings[username]["dark_mode"]
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
    print({"leaderboard": rankings[:10]})
    return {
        "leaderboard": rankings[:10]
    }

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=8000)