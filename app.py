from flask import Flask, request, redirect, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

from routes.lms_routes import lms

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# 🔥 REGISTER BLUEPRINT
app.register_blueprint(lms, url_prefix="/lms")

@app.route("/")
def home():
    return redirect("/lms")

# 🔥 LOGIN
@app.route("/lms/login", methods=["POST"])
def lms_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = mongo.db.offers.find_one({"lms_email": email})

    if not user or user.get("lms_password") != password:
        return "Invalid credentials"

    session["student_email"] = email

    return redirect("/lms/dashboard")

if __name__ == "__main__":
    app.run(debug=True, port=5001)