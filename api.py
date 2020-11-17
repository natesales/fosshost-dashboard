from os import urandom
import base64
from flask import Flask, request, jsonify
from pymongo import MongoClient
from functools import wraps

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["fh-dash"]

argon = PasswordHasher()

def get_random_key():
    return base64.b64encode(urandom(48)).decode().replace("=", "")

def get_args(*args):
    # Parse the request's JSON payload and return as a tuple of arguments.

    if request.json is None:
        # TODO: Replace this function with a decorator that handles this ValueError and returns a correct JSON error response
        raise ValueError("request body isn't valid JSON")

    payload = []

    for arg in args:
        try:
            arg_val = request.json[arg]
        except KeyError:
            raise ValueError("required argument \"" + str(arg) + "\" not supplied.")
        else:
            payload.append(arg_val)

    if len(payload) == 1:
        return payload[0]
    else:
        return tuple(payload)

@app.route("/register", methods=["POST"])
def register():
    try:
        name, url, email, nick, password, message = get_args("name", "url", "email", "nick", "password", "message")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    db["projects"].insert_one({
        "name": name,
        "url": url,
        "email": email,
        "nick": nick,
        "password": argon.hash(password),
        "message": message,
        "key": get_random_key(),
        "status": "pending"
    })

    # TODO: Send email

    return jsonify({"success": True, "message": "Your account has been registered. Please allow 24-48 hours for your request to be processed."})

@app.route("/login", methods=["POST"])
def login():
    try:
        email, password = get_args("email", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    project_doc = db["projects"].find_one({"email": email})
    if not project_doc:
        return jsonify({"success": "False", "message": "This user doesn't exist"})

    try:
        valid = argon.verify(project_doc["password"], password)
    except VerifyMismatchError:
        return jsonify({"success": False, "message": "Invalid username or password"})
    else:
        if valid:
            if project_doc["status"] == "active":
                return jsonify({"success": True, "message": project_doc["key"]})
            else:
                return jsonify({"success": False, "message": "This account is not active. If you have just submitted your registration, please allow 24-48 hours for account activation. Otherwise, contact us at https://fosshost.org/contact/ for more information."})
        else:
            return jsonify({"success": False, "message": "Invalid username or password"})


app.run(host="localhost", port=5001)
