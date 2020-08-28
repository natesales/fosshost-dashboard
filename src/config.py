# parser.py
# YAML config parser for IO
# Copyright © Nathan Sales 2020

import yaml
import terminal

CONFIG_FILE = "config.yml"

with open(CONFIG_FILE, 'r') as configfile:
    try:
        config_raw = yaml.safe_load(configfile)
        print(terminal.status.success, "Opened " + CONFIG_FILE)
    except Exception as e:  # Catch general exceptions to cover yaml.YAMLError and OS file access errors
        print(terminal.status.medium, "Config file " + CONFIG_FILE + " doesn't exist.")
        exit(1)

    # Default values
    name = "Unconfigured Proxmox IO Panel"
    hosts = []

    try:
        name = config_raw["name"]
    except KeyError:
        print(terminal.status.info, "Using default IO controller name")

    hosts = {}  # Public dict for host information

    try:
        _hosts = config_raw["hosts"]
        if len(_hosts) == 0:
            raise KeyError  # Trip the exception to be caught below
    except KeyError:
        print(terminal.status.medium, "No hosts configured.")
        exit(1)

    print(terminal.status.info, str(len(_hosts)) + " host(s) configured")

    for host in _hosts:
        if '/' in host or '&' in host:
            print(terminal.status.medium, "Hostnames should not contain URI-like syntax. Check " + host)
            exit(1)

        # Defaults
        username = "root@pam"
        port = 8006
        insecure = False

        try:
            username = _hosts[host]["username"]
        except KeyError:
            print(terminal.status.info, "Using username (root@pam) for host " + host)

        try:
            port = int(_hosts[host]["port"])
        except KeyError:
            print(terminal.status.info, "Using default port (8006) for host " + host)

        try:
            password = _hosts[host]["password"]
        except KeyError:
            print(terminal.status.medium, "No password configured for host " + host)
            exit(1)

        try:
            insecure = _hosts[host]["insecure"]
        except KeyError:
            print(terminal.status.info, "Using secure HTTPS verification for host " + host)

        host_uri = "https://" + host + ":8006/"
        hosts[host_uri] = {"username": username, "password": password, "insecure": insecure}
        print(terminal.status.success, "Added " + host_uri)