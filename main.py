import json
from email.mime.text import MIMEText
from functools import wraps
from os import environ
from smtplib import SMTP_SSL as SMTP

import requests
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import Flask, request, jsonify, make_response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from netboxapi import NetboxClient

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

argon = PasswordHasher()

app = Flask(__name__)

netbox = NetboxClient(environ["FHDASH_NETBOX_URL"], environ["FHDASH_NETBOX_TOKEN"], verify=False)


def get_args(*args):
    # Parse the request's JSON payload and return as a ;tuple of arguments.

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


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cookie = request.headers.get("Cookie")
        if not cookie:
            return jsonify({"success": False, "message": "Not Authenticated"})

        api_key = request.headers.get("Cookie").split("apikey=")[1]

        project = netbox.find_project("key", api_key)
        if not project:
            return jsonify({"success": False, "message": "Not Authenticated"})
        elif project["status"] != "active":
            return jsonify({"success": False, "message": "Your account is not active"})
        else:
            return f(*args, **kwargs, project=project)

    return decorated_function


def send_email(to, subject, body):
    print("Sending email to", to)

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = environ["FHDASH_SMTP_USER"]

    server = SMTP(environ["FHDASH_SMTP_SERVER"])
    server.login(environ["FHDASH_SMTP_USER"], environ["FHDASH_SMTP_PASSWORD"])
    server.sendmail(environ["FHDASH_SMTP_USER"], to, msg.as_string())
    server.quit()
    print("Sent")


def create_ticket(name, email, subject, body):
    print("Sending " + body + " to " + email)
    r = requests.post(environ["FHDASH_HELPY_URI"], data='data=' + json.dumps({
        "message": {
            "kind": "ticket",
            "subject": subject,
            "body": body,
            "channel": "web"
        },
        "customer": {
            "fullName": name,
            "emailAddress": email,
            "company": name
        }
    }))

    print(r.text)


@app.route("/register", methods=["POST"])
def register():
    try:
        name, url, email, nick, password, message = get_args("name", "url", "email", "nick", "password", "message")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    # Add the project to netbox
    response = netbox.add_project(name, url, email, nick, argon.hash(password), message, "pending")

    if str(response.status_code)[0] == "2":  # HTTP 2xx
        create_ticket(name, email, f"({name}) Account Request", f"Name: {name}\nURL: {url}\nEmail: {email}\nNick: {nick}\nMessage: {message}")
        return jsonify({"success": True, "message": "Your account has been registered. Please allow 24-48 hours for your request to be processed."})

    else:
        return jsonify({"success": False, "message": str(response.json())})


@app.route("/login", methods=["POST"])
def login():
    try:
        email, password = get_args("email", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    project_data = netbox.find_project("email", email)
    if not project_data:
        return jsonify({"success": False, "message": "Account not found"})

    # Compare password hash
    try:
        valid = argon.verify(project_data["password"], password)
        if not valid:
            raise VerifyMismatchError
    except VerifyMismatchError:
        return jsonify({"success": False, "message": "Invalid username or password"})

    if project_data["status"] == "active":
        resp = make_response(jsonify({"success": True, "message": project_data["key"]}))
        resp.set_cookie("apikey", project_data["key"])
        return resp
    else:
        return jsonify({"success": False, "message": "This account is not active. If you have just submitted your registration, please allow 24-48 hours for account activation. Otherwise, contact us at https://fosshost.org/contact/ for more information."})


@app.route("/auth/check")
@auth_required
def auth_check(project):
    # Check if a user is logged in (the auth_check decorator will return a negative response, so the following is only the authenticated response)
    return jsonify({"success": True, "message": project})


@app.route("/auth/logout")
def auth_logout():
    # Log a user out
    resp = make_response(jsonify({"success": True, "message": "Logged out successfully"}))
    resp.set_cookie("apikey", "")
    return resp


@app.route("/auth/change", methods=["POST"])
@auth_required
def auth_change(project):
    try:
        password = get_args("password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    netbox.change_password(project, argon.hash(password))

    return jsonify({"success": True, "message": f"Password updated"})


@app.route("/auth/add_key", methods=["POST"])
@auth_required
def auth_add_key(project):
    try:
        key = get_args("key")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not (key.startswith("ssh-rsa") or key.startswith("ssh-ed25519")):
        return jsonify({"success": False, "message": "Invalid SSH key. Keys must be in ssh-rsa or ssh-ed25519 format."})

    netbox.add_key(project, key)

    return jsonify({"success": True, "message": "Your key has been added"})


@app.route("/virt/list")
@auth_required
def virt_list(project):
    return netbox.list_vms(project)


@app.route("/virt/deprovision", methods=["POST"])
@auth_required
def virt_deprovision(project):
    try:
        hypervisor, hostname = get_args("hypervisor", "hostname")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    create_ticket(project["name"], project["email"], f"({project['name']}) Deprovisioning Request", f"Hostname: {hostname}\nHypervisor: {hypervisor}")
    return jsonify({"success": True, "message": f"Your deprovisioning request has been received. Please allow 24-48 hours for us to review your request."})


@app.route("/request", methods=["POST"])
@auth_required
def infra_request(project):
    try:
        service, message = get_args("service", "message")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not project.get("ssh-keys") or len(project.get("ssh-keys")) == 0:
        return jsonify({"success": False, "message": "Please add an SSH key to your account before requesting infrastructure. Click the 'Profile and Security' tab on the left side to add one!"})

    print(message)
    create_ticket(project["name"], project["email"], f"({project['name']}) Infrastructure Request", f"Service: {service}\nMessage: {message}")
    return jsonify({"success": True, "message": f"Your infrastructure request has been received. Please allow 24-48 hours for us to review your request."})


app.run(host="localhost", port=8084, debug=True)
