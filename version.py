#!/usr/bin/python3
import sys
import requests
from pkg_resources import parse_version
from toggle.__init__ import __version__

URL = "https://api.github.com/repos/intelligent-agent/toggle/releases/latest"

def get_local_version():
    return __version__

def get_remote_version():
    r = requests.get(URL)
    return r.json()["tag_name"]

def get_version():
    local_version = get_local_version()
    remote_version = get_remote_version()
    # Print local, remote and return code as pr OctoPrints request.
    print(local_version)
    print(remote_version)
    if parse_version(remote_version) > parse_version(local_version):
        sys.exit(0)
    sys.exit(1)

if __name__ == '__main__':
  get_version()