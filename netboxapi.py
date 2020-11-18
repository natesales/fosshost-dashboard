import base64
import json
from os import urandom

import requests


def get_random_key():
    return base64.b64encode(urandom(48)).decode().replace("=", "")


class NetboxClient:
    def __init__(self, host: str, api_key: str, verify=True):
        self.host = host
        self.verify = verify
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + api_key
        }

    def _get(self, route):
        return requests.get(self.host + route, headers=self.headers, verify=self.verify)

    def _post(self, route, data=None):
        if data is None:
            data = {}
        return requests.post(self.host + route, headers=self.headers, verify=self.verify, json=data)

    def _patch(self, route, data=None):
        if data is None:
            data = {}
        return requests.patch(self.host + route, headers=self.headers, verify=self.verify, json=data)

    # Main

    def add_project(self, name, url, email, nick, password, message, status):
        return self._post("tenancy/tenants/", data={
            "name": name,
            "slug": "".join(filter(str.isalnum, name.replace(" ", "-"))),
            "group": 3,
            "comments": json.dumps({
                "url": url,
                "email": email,
                "nick": nick,
                "password": password,
                "message": message,
                "status": status,
                "key": get_random_key()
            })
        })

    def find_project(self, k, v):
        for project in self._get("tenancy/tenants/?group=projects").json()["results"]:
            project_data = json.loads(project["comments"])
            if project_data[k] == v:
                project_data["name"] = project["name"]
                project_data["slug"] = project["slug"]
                project_data["id"] = project["id"]
                return project_data
        return None

    def change_password(self, project, password):
        _id = str(project["id"])
        _name = str(project["name"])
        _slug = str(project["slug"])
        del project["id"]
        del project["name"]
        del project["slug"]
        project["password"] = password

        return self._patch("tenancy/tenants/" + _id + "/", data={
            "name": _name,
            "slug": _slug,
            "comments": json.dumps(project)
        })

    def add_key(self, project, key):
        _id = str(project["id"])
        _name = str(project["name"])
        _slug = str(project["slug"])
        del project["id"]
        del project["name"]
        del project["slug"]
        if "ssh-keys" in project:
            project["ssh-keys"].append(key)
        else:
            project["ssh-keys"] = [key]

        return self._patch("tenancy/tenants/" + _id + "/", data={
            "name": _name,
            "slug": _slug,
            "comments": json.dumps(project)
        })

    def list_vms(self, project):
        return self._get("virtualization/virtual-machines/?tenant=" + project["slug"]).json()
