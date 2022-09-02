import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Introduction to page"""
    current_user = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE id = ?", current_user)
    username = user_data[0]["username"]
    return render_template("index.html", username=username)


@app.route("/BMI", methods=["GET", "POST"])
@login_required
def BMI():
    """BMI calculations"""
    if request.method == "POST":
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        bmi = round(weight / (height * height), 1)
        current_user = session["user_id"]
        # Insert BMI into database
        db.execute("UPDATE users SET BMI = ? WHERE id = ?", bmi, current_user)
        plan = ""
        if bmi > 25:
            plan = "Fat loss"
        elif bmi < 18.5:
            plan = "Muscle gain"
        else:
            plan = "Stay fit"
        return render_template("success.html", plan=plan)
    else:
        return render_template("BMI.html")


@app.route("/Myplan")
@login_required
def Myplan():
    """Show user's plan"""
    current_user = session["user_id"]
    user_bmi = db.execute("SELECT BMI FROM users WHERE id = ?", current_user)
    actual_bmi = user_bmi[0]["BMI"]
    if not actual_bmi:
        return apology("Enter your BMI", 403)
    Myplan = ""
    if actual_bmi > 25:
        Myplan = "Fat loss"
    elif actual_bmi < 18.5:
        Myplan = "Muscle gain"
    else:
        Myplan = "Stay fit"
    return render_template("Myplan.html", Myplan=Myplan)


@app.route("/plan")
@login_required
def plan():
    """Show all plans"""

    return render_template("plan.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Check if user has a BMI
        bmi = rows[0]["BMI"]
        if not bmi:
            return render_template("BMI.html")
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST
    if request.method == "POST":
        # Check if username typed a username
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Check if username typed a password
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Check if user confirmed his password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        # Hash the password
        hashpw = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)
        # Insert info into database
        username = request.form.get("username")
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hashpw)
        except:
            return apology("duplicate username")
        # return to login if successful
        return redirect("/login")
    else:
        return render_template("register.html")
