import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from functools import wraps
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import json
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# @login_required decorator
# https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/#login-required-decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # no "user" in session
        if "user" not in session:
            flash("You Must Log In To View This Page")
            return redirect(url_for("login"))
        # user is in session
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@app.route("/home")
def home():
    profile = mongo.db.jobseekers.find()
    return render_template("home.html", profile=profile)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.jobseekers.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            flash("Account with such an email is already registered")
            return redirect(url_for("employee_register"))

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
                "sector": request.form.getlist("sector"),
                "sector_other": request.form.get("sector_other"),
                "experience": request.form.get("experience1"),
                "education": request.form.get("education1"),
                "contact_preference": request.form.getlist("contact_preference"),
                "accommodations": request.form.get("accommodations"),
                "avatar": request.form.get("avatar")
            }
            mongo.db.jobseekers.insert_one(register)
        session["user"] = request.form.get("email")
        flash("Registration Successful!")
        return redirect(url_for("employee_profile", username=session["user"]))

    return render_template("chatbot.html")


@app.route("/employee_register", methods=["GET", "POST"])
def employee_register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.jobseekers.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            flash("Account with such an email is already registered")
            return redirect(url_for("employee_register"))

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
                "sector": request.form.getlist("sector"),
                "sector_other": request.form.getlist("sector_other"),
                "experience": request.form.get("experience1"),
                "education": request.form.get("education1"),
                "contact_preference": request.form.getlist("contact_preference"),
                "accommodations": request.form.get("accommodations"),
                "avatar": request.form.get("avatar")
            }
            mongo.db.jobseekers.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email")
        flash("Registration Successful!")
        return redirect(url_for("employee_profile", username=session["user"]))

    sectors = list(mongo.db.sectors.find())
    return render_template("employee_register.html", sectors=sectors)


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
        return redirect(url_for("employer_profile", username=session["user"]))

    return render_template("employer_register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_employee", methods=["GET", "POST"])
def login_employee():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.jobseekers.find_one(
            {"email": request.form.get("email")})
        name = existing_user["full_name"]

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email")
                flash("Welcome, {}!".format(name))
                return redirect(url_for(
                    "employee_profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login_employee", username=name))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login_employee"))

    return render_template("login_employee.html")


@app.route("/login_employer", methods=["GET", "POST"])
def login_employer():
    if request.method == "POST":
        # check if username exists in db
        email = request.form.get("email")
        existing_user = mongo.db.companies.find_one(
            {"email": email})
        name = existing_user["full_name"]

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email")
                flash("Welcome, {}!".format(name))
                return redirect(url_for(
                    "employer_profile", username=email))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login_employer"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login_employer"))

    return render_template("login_employer.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = mongo.db.companies.find_one({"email": username})
    if user:
        return redirect(url_for(
            "employer_profile", username=username))
    return redirect(url_for(
        "employee_profile", username=username))


@app.route("/employer_profile/<username>")
@login_required
def employer_profile(username):
    if session["user"] == username:
        user = mongo.db.companies.find_one({"email": username})
        return render_template(
            "employer_profile.html", user=user)
    return redirect(url_for("home"))


@app.route("/employee_profile/<username>")
@login_required
def employee_profile(username):
    if session["user"] == username:
        sectors = list(mongo.db.sectors.find())
        user = mongo.db.jobseekers.find_one({"email": username})
        return render_template(
            "employee_profile.html", user=user, sectors=sectors)
    return redirect(url_for("home"))


@app.route("/candidate_details/<username>")
@login_required
def candidate_details(username):
    candidate = mongo.db.jobseekers.find_one({"email": username})
    return render_template("candidate_details.html", candidate=candidate)


@app.route("/all_candidates")
def all_candidates():
    all_candidates = mongo.db.jobseekers.find()
    return render_template(
        "all_candidates.html", all_candidates=all_candidates)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    all_candidates = list(mongo.db.jobseekers.find({"$text": {"$search": query}}))
    return render_template("all_candidates.html", all_candidates=all_candidates)



@app.route("/employer_update/<username>", methods=["GET", "POST"])
@login_required
def employer_update(username):
    if session["user"] == username:
        if request.method == "POST":
            full_name = request.form.get("full_name").lower()
            company_name = request.form.get("company_name").lower()
            phone = request.form.get("phone")
            city = request.form.get("city").lower()
            country = request.form.get("country").lower()

            mongo.db.companies.update_one(
                {"email": username}, {"$set": {"full_name": str(full_name).strip("( , ' )"),
                                               "company_name": str(company_name).strip("( , ' )"),
                                               "phone": str(phone).strip("( , ' )"),
                                               "city": str(city).strip("( , ' )"),
                                               "country": str(country).strip("(,')")}})
            flash("Your Profile Was Successfully Updated")
            return redirect(url_for(
                "employer_profile", username=username))
    return redirect(url_for("home"))


@app.route("/employee_update/<username>", methods=["GET", "POST"])
@login_required
def employee_update(username):
    if session["user"] == username:
        if request.method == "POST":
            full_name = request.form.get("full_name").lower()
            phone = request.form.get("phone")
            city = request.form.get("city").lower()
            country = request.form.get("country").lower()
            sector = request.form.getlist("sector")
            sector_other = request.form.get("sector_other")
            description = request.form.get("description")
            experience = request.form.get("experience1")
            education = request.form.get("education1")
            contact_preference = request.form.getlist("contact_preference")
            accommodations = request.form.get("accommodations")

            mongo.db.jobseekers.update_one(
                {"email": username}, {"$set": {"full_name": str(full_name).strip("( , ' )"),
                                               "phone": str(phone).strip("( , ' )"),
                                               "city": str(city).strip("( , ' )"),
                                               "country": str(country).strip("(,')"),
                                               "sector": sector,
                                               "sector_other": str(sector_other).strip("( , ' )"),
                                               "description": str(description).strip("( , ' )"),
                                               "experience": str(experience).strip("( , ' )"),
                                               "education": str(education).strip("( , ' )"),
                                               "contact_preference": contact_preference,
                                               "accommodations": str(accommodations).strip("( , ' )")}})
            flash("Your Profile Was Successfully Updated")
            return redirect(url_for(
                "employee_profile", username=username))
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
