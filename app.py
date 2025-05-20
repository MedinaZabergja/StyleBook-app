from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

app.config["MONGO_URI"] = "mongodb://localhost:27017/stylebook_db"

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/stylebook"
mongo = PyMongo(app)

# Home page
@app.route("/")
def home():
    return render_template("home.html")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form["username"]})

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("signup"))

        hashed_pw = generate_password_hash(request.form["password"])
        users.insert_one({
            "username": request.form["username"],
            "password": hashed_pw
        })
        flash("Signup successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        user = users.find_one({"username": request.form["username"]})

        if user and check_password_hash(user["password"], request.form["password"]):
            session["username"] = user["username"]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials.")
            return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
