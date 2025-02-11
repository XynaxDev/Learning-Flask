from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        return f"Hello {user}, How are you? what"
    else:
        return render_template("login.html")


@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    return render_template("forgot_password.html")


# Sessions




# @app.route("/")
# def user():
#     return render_template("index.html", content = ["ajith","sudhir","sawan"])

# @app.route("/admin")
# def admin():
#     return redirect(url_for("user",name="Admin!"))

if __name__ == "__main__":
    app.run(debug=True)
