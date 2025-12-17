from flask import Flask, session, redirect, url_for, flash , request , render_template
from routes.pages import pages
from routes.api import api
from routes.viewer import viewer

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(pages)
app.register_blueprint(api)
app.register_blueprint(viewer)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # basic authentication for now

        user_name = os.getenv("BLOG_ADMIN_USERNAME")
        user_pwd = os.getenv("BLOG_ADMIN_PASSWORD")

        print(username , password , user_name , user_pwd)
        
        if username == user_name and password == user_pwd:
            session["user"] = {"username": username}
            return redirect(url_for("pages.dashboard"))
        else:
            flash("Invalid credentials", "error")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
