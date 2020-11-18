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
                return project_data
        return None

    def list_vms(self):
        return self._get("virtualization/virtual-machines/?tenant=delivrdev").json()