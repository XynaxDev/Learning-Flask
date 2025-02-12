from flask import Flask,redirect,url_for,render_template,request,session,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "apak143"
app.permanent_session_lifetime = timedelta(minutes=5)

# In session : it stores data temporarily on the the website 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

# Sessions
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True # It considers that the data will stay on the website tile the lifetime 
        user = request.form["username"]
        session["user"] = user
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    return render_template("forgot_password.html")




@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user = user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out successfully!","info")
    session.pop("user",None)
    return redirect(url_for("login")) 



if __name__ == "__main__":
    app.run(debug=True)
