from flask import Flask, render_template, session, request, redirect, url_for
import json
import os
from Backend.Helpers.users import *
from Backend.utils.constants import *

def init_db():
    os.makedirs(os.path.dirname(USER_DB_PATH), exist_ok=True)

    if not os.path.exists(USER_DB_PATH) or os.path.getsize(USER_DB_PATH) == 0:
        with open(USER_DB_PATH, "w") as f:
            json.dump([], f)

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
    
@app.context_processor
def inject_user():
    return {
        "user": session.get("user")
    }

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST request
    username = request.form.get("username")
    password = request.form.get("password")

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
        return render_template("register.html",error="Account already exists")

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True,port=8000)