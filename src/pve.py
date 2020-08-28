# pve.py
# Proxmox VE HTTP API wrapper for Python
# Copyright © Nathan Sales 2020

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import terminal
import ipam


class PVEError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "PVEError " + str(self.message)
        else:
            return "PVEError"


class Server:
    def __init__(self, host, username, password, suppress_insecure_cert_warning=False):
        if '@' not in username:
            print(terminal.status.medium, "Usernames must specify an authentication realm")

        self.url = host + "api2/json/"
        self.authorization = {"username": username, "password": password}
        self.suppress_insecure_cert_warning = not suppress_insecure_cert_warning
        self.headers = {}
        self.node = ""  # Node name, declared here and initialized in the _login method

        # Proxmox uses self-signed ssl certs, which are invalid as far as requests is concerned. This statement suppresses these invalid warnings if enabled.
        if suppress_insecure_cert_warning:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def login(self):
        _init_response = requests.post(self.url + "access/ticket", data=self.authorization, verify=self.suppress_insecure_cert_warning)
        try:
            if _init_response.json()["data"] is None:
                return False
            _ticket = _init_response.json()["data"]["ticket"]
            _csrf_token = _init_response.json()["data"]["CSRFPreventionToken"]
        except KeyError as e:
            raise PVEError("Error getting authentication tokens", e)

        self.headers = {"CSRFPreventionToken": _csrf_token, "Cookie": "PVEAuthCookie=" + _ticket}
        self.node = self._get("nodes").json()["data"][0]["node"]

        return True

    def _get(self, endpoint, data=None):
        print("GET", self.url + endpoint)
        return requests.get(self.url + endpoint, data=data, headers=self.headers, verify=self.suppress_insecure_cert_warning)

    def _post(self, endpoint, data=None):
        print("POST", self.url + endpoint)
        return requests.post(self.url + endpoint, data=data, headers=self.headers, verify=self.suppress_insecure_cert_warning)

    def _put(self, endpoint, data=None):
        return requests.put(self.url + endpoint, data=data, headers=self.headers, verify=self.suppress_insecure_cert_warning)

    def _delete(self, endpoint, data=None):
        return requests.delete(self.url + endpoint, data=data, headers=self.headers, verify=self.suppress_insecure_cert_warning)

    # -- User Management --

    def new_user(self, username, password):
        return self._post("/access/users", data={"userid": username, "password": password})

    # -- Query Methods --

    def list(self):
        return self._get("nodes/" + self.node + "/qemu")

    def authenticated(self):
        return self._get("nodes/" + self.node + "/qemu").status_code == 200

    # -- Control methods --

    # Create a new VM
    def new(self):
        newid = self._get("cluster/nextid").json()["data"]

        response = self._post("nodes/" + self.node + "/qemu/117/clone", data={
            "newid": newid,
            "full": 1
        })
        print(response.text)

    # Configure a VM
    def config(self, vmid, hostname, password):
        _ips = ipam.get(hostname)
        ipv4 = _ips[0]
        ipv6 = _ips[1]

        response = self._post("/nodes/" + self.node + "/qemu/" + str(vmid) + "/config", data={
            "name": hostname,
            "onboot": 1,  # Start on boot
            "citype": "nocloud",
            # TODO: Extract gateways to config file
            "ipconfig0": "gw=10.0.0.1,ip=" + ipv4 + ",gw6=2001:db8::1,ip6=" + ipv6,
            "ciuser": "root",
            "cipassword": password
        })
        print(response.text)

    # Authorize a user to use a VM
    def authorize(self, vmid, user):
        response = self._put("access/acl/", data={"users": user, "path": "/vms/" + str(vmid), "roles": "PVEVMUser"})
        print(response.text)
        return response

    # Start a VM
    def start(self, vmid):
        response = self._post("nodes/" + self.node + "/qemu/" + str(vmid) + "/status/start")
        print(response.text)
        return response

    # Stop a VM
    def stop(self, vmid):
        response = self._post("nodes/" + self.node + "/qemu/" + str(vmid) + "/status/stop")
        print(response.text)
        return response

    # Shutdown a VM
    def shutdown(self, vmid):
        response = self._post("nodes/" + self.node + "/qemu/" + str(vmid) + "/status/shutdown")
        print(response.text)
        return response

    # Reboot a VM
    def reboot(self, vmid):
        response = self._post("nodes/" + self.node + "/qemu/" + str(vmid) + "/status/reboot")
        print(response.text)
        return response

    # Reset a VM
    def reset(self, vmid):
        response = self._post("nodes/" + self.node + "/qemu/" + str(vmid) + "/status/reset")
        print(response.text)
        return response

    # Delete a VM
    def delete(self, vmid):
        response = self._delete("nodes/" + self.node + "/qemu/" + str(vmid))
        print(response.text)
        return response
