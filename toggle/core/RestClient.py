import time
import requests
import json

import logging


class RestClient:
  def __init__(self, config):
    self.config = config
    self._prefix = "/api"
    self.load_parameters()

  def load_parameters(self):
    self._host = self.config.get("Server", "host")
    self._port = self.config.get("Server", "port")
    self._api_key = self.config.get("OctoPrint", "authentication")
    self._headers = {'Content-Type': 'application/json', 'X-Api-Key': self._api_key}
    # Whoever the session turned out to belong to - autologin decides it,
    # not the config, so the socket auth must use this rather than "user".
    self.session_user = None

  # What default.cfg ships until toggle-runfirst fills local.cfg in.
  PLACEHOLDER = "REPLACE_ME"

  def credentials_ready(self):
    """False while OctoPrint has not been set up yet.

    A fresh image ships default.cfg's placeholders and an empty API key. Those
    cannot be filled in until OctoPrint's setup wizard has created the first
    user, because only then can toggle-runfirst add ours - and the wizard waits
    on a human.

    Posting a login in the meantime cannot succeed, and posting one every second
    is worse than useless: OctoPrint's brute force protection starts answering
    429, and it then refuses the real login too, once it finally arrives. Seen
    on a bench board that had been sitting at the wizard - the endpoint had to
    be freed by restarting OctoPrint before a valid key would work.
    """
    password = self.config.get("OctoPrint", "password")
    return (bool(self._api_key) and self._api_key != self.PLACEHOLDER
            and bool(password) and password != self.PLACEHOLDER)

  def login(self):
    """A session for the push socket, without credentials where possible.

    OctoPrint is configured with accessControl.autologinLocal, so a request that
    arrives from this machine is already logged in as accessControl.autologinAs
    by the time it is handled. A passive login just asks who that turned out to
    be and returns the session the socket auth needs - no password, no API key,
    nothing to keep in step with OctoPrint's password hashing.

    That last part is not hypothetical. toggle-runfirst wrote its user's password
    as sha512(password + salt), OctoPrint 1.11 stores argon2id, and the two never
    matched: the toggle user existed, in the right group, with a hash that could
    not authenticate. Not sending a password removes the whole class of that.

    The GET is doing two jobs: it collects the double-submit CSRF cookie that
    /api/login demands, and it is the request autologin acts on. Use a Session so
    the cookie it sets is resent on the POST below.

    Falls back to user and password, for an OctoPrint without autologin
    configured - but only once those are real, see credentials_ready().
    """
    session = requests.Session()
    try:
      session.get(f"http://{self._host}:{self._port}/")
    except requests.ConnectionError:
      logging.warning("Cannot reach OctoPrint at %s:%s", self._host, self._port)
      return "INVALID-SESSION"

    csrf_token = next(
      (v for k, v in session.cookies.items() if k.startswith("csrf_token")),
      None
    )
    headers = {'Content-Type': 'application/json'}
    if csrf_token:
      headers['X-CSRF-Token'] = csrf_token

    # Passive first, and unconditionally: it sends no credentials, so it cannot
    # fail an authentication attempt and cannot count against OctoPrint's brute
    # force protection.
    try:
      r = session.post(self._build_url("login"),
                       data=json.dumps({"passive": True}), headers=headers)
      if r.status_code == 200:
        d = r.json()
        if d.get("session") and d.get("name"):
          self.session_user = d["name"]
          logging.info("Logged in as %s (%s)",
                       d["name"], d.get("_login_mechanism", "passive"))
          return d["session"]
    except (requests.RequestException, ValueError) as e:
      logging.warning("Passive login failed (%s), trying credentials", e)

    if not self.credentials_ready():
      return "INVALID-SESSION"

    user = self.config.get("OctoPrint", "user")
    password = self.config.get("OctoPrint", "password")
    r = session.post(self._build_url("login"),
                     data=json.dumps({'user': user, 'pass': password}),
                     headers=headers)
    if r.status_code == 200:
      self.session_user = user
      return r.json()["session"]
    logging.warning("Authentication failed! Check username and password + CORS")
    return "INVALID-SESSION"

  def connection_ok(self):
    r = requests.get(self._build_url("version"), headers=self._headers)
    return r.status_code == 200

  def start_job(self):
    data = json.dumps({'command': 'start'})
    r = requests.post(self._build_url("job"), data=data, headers=self._headers)
    return r.status_code == 204

  def pause_job(self):
    data = json.dumps({'command': 'pause'})
    r = requests.post(self._build_url("job"), data=data, headers=self._headers)
    return r.status_code == 204

  def cancel_job(self):
    data = json.dumps({'command': 'cancel'})
    r = requests.post(self._build_url("job"), data=data, headers=self._headers)
    return r.status_code == 204

  def resume_job(self):
    data = json.dumps({'command': 'pause'})
    r = requests.post(self._build_url("job"), data=data, headers=self._headers)
    return r.status_code == 204

  def send_gcode(self, cmd):
    url = self._build_url("printer/command")
    data = json.dumps({'command': cmd})
    r = requests.post(url, data=data, headers=self._headers)
    return r.status_code == 204

  def start_preheat(self):
    bed_temp = self.config.get("Preheat", "bed_temp")
    tool_0 = self.config.get("Preheat", "t0_temp")
    tool_1 = self.config.get("Preheat", "t1_temp")
    self.set_bed_temp(bed_temp)
    self.set_tool_temp(0, tool_0)
    self.set_tool_temp(1, tool_1)

  def stop_preheat(self):
    self.set_bed_temp(0)
    self.set_tool_temp(0, 0)
    self.set_tool_temp(1, 0)

  def set_bed_temp(self, temp):
    url = self._build_url("printer/bed")
    data = json.dumps({'command': 'target', 'target': int(float(temp))})
    r = requests.post(url, data=data, headers=self._headers)
    return r.status_code == 204

  def set_tool_temp(self, tool_nr, temp):
    url = self._build_url("printer/tool")
    data = json.dumps({'command': 'target', 'targets': {'tool' + str(tool_nr): int(float(temp))}})
    r = requests.post(url, data=data, headers=self._headers)
    return r.status_code == 204

  def select_file(self, filename):
    url = self._build_url("files/local/" + filename)
    data = json.dumps({'command': 'select'})
    r = requests.post(url, data=data, headers=self._headers)
    return r.status_code == 204

  # Jog the printer
  def jog(self, amount):
    data = json.dumps({'command': 'jog', **amount})
    r = requests.post(self._build_url("printer/printhead"), data=data, headers=self._headers)
    return r.status_code == 204

  # Home selected axes
  def home(self, axes):
    data = json.dumps({'command': 'home', 'axes': axes})
    r = requests.post(self._build_url("printer/printhead"), data=data, headers=self._headers)
    return r.status_code == 204

  def extrude(self, amount):
    data = json.dumps({'command': 'extrude', 'amount': amount})
    r = requests.post(self._build_url("printer/tool"), data=data, headers=self._headers)
    return r.status_code == 204

  def select_tool(self, tool):
    data = json.dumps({'command': 'select', 'tool': tool})
    r = requests.post(self._build_url("printer/tool"), data=data, headers=self._headers)
    return r.status_code in [200, 204]

  def get_list_of_files(self):
    try:
      r = requests.get(self._build_url("files"), headers=self._headers)
    except requests.ConnectionError as e:
      logging.warning("Connection error")
      return {'files': []}
    if r.status_code in [200, 204]:
      return r.json()
    logging.warning("Unable to contact OctoPrint by REST. "
                    "Check your API key (currently '" + self._api_key + "'")
    return {'files': []}

  def download_model(self, url):
    try:
      r = requests.get(url)
    except requests.ConnectionError as e:
      return None
    if r.status_code == 200:
      logging.debug("Download OK")
      return r.content
    logging.warning("Unable to download file. Got response: " + r.status_code)
    return None

  def get_slicers(self):
    r = requests.post(self._build_url("slicing"), headers=self._headers)
    if r.status_code == 200:
      return r.json()
    logging.warning("Unable to gt slicers: " + r.status_code)
    return {}

  def _build_url(self, path):
    return f"http://{self._host}:{self._port}/api/{path}"
