from email.mime.text import MIMEText
from functools import wraps
from os import environ
from smtplib import SMTP_SSL as SMTP

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import Flask, request, jsonify, make_response
from jinja2 import Template

from netboxapi import NetboxClient

argon = PasswordHasher()

app = Flask(__name__)
netbox = NetboxClient(environ["FHDASH_NETBOX_URL"], environ["FHDASH_NETBOX_TOKEN"], verify=False)

with open("templates/application_submitted.j2") as application_submitted_template_file:
    application_submitted_template = Template(application_submitted_template_file.read())

with open("templates/infra_request.j2") as infra_request_template_file:
    infra_request_template = Template(infra_request_template_file.read())


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


@app.route("/register", methods=["POST"])
def register():
    try:
        name, url, email, nick, password, message = get_args("name", "url", "email", "nick", "password", "message")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    # Add the project to netbox
    response = netbox.add_project(name, url, email, nick, argon.hash(password), message, "pending")

    print(response.status_code)
    if str(response.status_code)[0] == "2":  # HTTP 2xx
        send_email(["nate@fosshost.org"], "[FOSSHOST] Project Application", application_submitted_template.render(name=name, email=email, nick=nick, message=message))
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

    print(netbox.change_password(project, argon.hash(password)).json())

    return jsonify({"success": True, "message": f"Password updated"})


@app.route("/virt/list")
@auth_required
def virt_list(project):
    return netbox.list_vms()


@app.route("/virt/deprovision", methods=["POST"])
@auth_required
def virt_deprovision(project):
    try:
        hypervisor, hostname = get_args("hypervisor", "hostname")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    # TODO: Send email
    return jsonify({"success": True, "message": f"Deprovisioning {hostname} on {hypervisor}. Please allow 24-48 hours for us to review your request."})


@app.route("/request", methods=["POST"])
@auth_required
def infra_request(project):
    try:
        service, message = get_args("service", "message")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    send_email(["nate@fosshost.org"], "[FOSSHOST] Infrastructure Request", infra_request_template.render(name=project["name"], service=service, message=message))
    return jsonify({"success": True, "message": f"{project['name']} requested {service} with {message}. Please allow 24-48 hours for us to review your request."})


app.run(host="localhost", port=8084, debug=True)
