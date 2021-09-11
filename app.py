import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    profile = mongo.db.jobseekers.find()
    return render_template("home.html", profile=profile)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/employee_register", methods=["GET", "POST"])
def employee_register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.jobseekers.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Account with such an email is already registered")
            return redirect(url_for("register"))
        
        sector = request.form.get("sector")
        if sector == "other":
            sector = request.form.get("sector_other")

        if (request.form.get("password1") == request.form.get("password2")):
            register = {
                "full_name": request.form.get("full_name").lower(),
                "password": generate_password_hash(
                    request.form.get("password1")),
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "city": request.form.get("city").lower(),
                "country": request.form.get("country").lower(),
                "description": request.form.get("description"),
                "sector": sector,
                "experience": request.form.get("experience1"),
                "education": request.form.get("education1"),
                "contact_preference": request.form.get("contact_preference"),
                "accommodations": request.form.get("accommodations"),
                "is_employer": False
            }
            mongo.db.jobseekers.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("home"))
        # return redirect(url_for("profile", username=session["user"]))
    return render_template("employee_register.html")


@app.route("/employer_register", methods=["GET", "POST"])
def employer_register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.companies.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("This company is already registered")
            return redirect(url_for("register"))

        if (request.form.get("password1") == request.form.get("password2")):
            register = {
                "full_name": request.form.get("full_name").lower(),
                "company_name": request.form.get("company_name").lower(),
                "password": generate_password_hash(
                    request.form.get("password1")),
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "city": request.form.get("city").lower(),
                "country": request.form.get("country").lower(),
                "is_employer": True
            }
            mongo.db.companies.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("home"))
        # return redirect(url_for("profile", username=session["user"]))
    return render_template("employer_register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}!".format(
                    request.form.get("username")))
                if existing_user.is_employer:
                    return redirect(url_for(
                        "employer_profile", username=session["user"]))
                else:
                    return redirect(url_for(
                        "jobseeker_profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
