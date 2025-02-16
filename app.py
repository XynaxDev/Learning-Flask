from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from models import Users,db

app = Flask(__name__)
app.secret_key = "apak143"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db.init_app(app)

# Session : it stores data temporarily on the website 
@app.route("/")
def home():
    return render_template("index.html")

# Sessions
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True  # It considers that the data will stay on the website for the duration of the session lifetime 
        user = request.form["username"]
        password = request.form["password"]

        # if not (password and user):
        #     flash("Username and password is required to login!", "danger")
        #     return redirect(url_for("login"))
        
        session["user"] = user

        found_user = Users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
            session["name"] = found_user.name
        else:
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit()
            session["name"] = user
            session["email"] = ""

        flash("Login Successful!", "success")
        return redirect(url_for("user"))       
    else:
        if "user" in session:
            flash("Already Logged in!", "success")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if "user" in session:
        current_user = session["user"]

        if request.method == "POST":
            # FIX: Swap the retrieval so that 'email' comes from the "email" field and 'name' from the "name" field.
            email = request.form.get("email")
            name = request.form.get("name")

            if (email or name):
                session["email"] = email
                session["name"] = name

            found_user = Users.query.filter_by(name=current_user).first()
            if found_user:
                found_user.email = session["email"]
                found_user.name = session["name"]
                db.session.commit()

            flash("Name and email were saved!", "success")
            return redirect(url_for("dashboard"))
            # name = request.form["name"]
            # session["name"] = name
            # found_user = Users.query.filter_by(name = user).first()
            # found_user.name = name
            # db.session.commit()

        else:
            if "email" not in session or "name" not in session:
                found_user = Users.query.filter_by(name=current_user).first()
                if found_user:
                    session["email"] = found_user.email
                    session["name"] = found_user.name
            return render_template("user.html", name=session["name"], email=session["email"])
    else:
        flash("You are not logged in!", "fail")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        current_user = session["user"]
        found_user = Users.query.filter_by(name=current_user).first()
        if found_user:
            if "email" in session:
                found_user.email = session["email"]
            if "name" in session:
                found_user.name = session["name"]
            db.session.commit()

        flash("You have been logged out successfully!", "success")
        session.pop("user", None)
        session.pop("email", None)
        session.pop("name", None)
        return redirect(url_for("login"))
    else:
        flash("You have already logged out!")
        return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "name" in session and "email" in session:
        return render_template("dashboard.html", values=Users.query.all())
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
