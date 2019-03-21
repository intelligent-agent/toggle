import time
import requests
import json

import logging
""" Rest API Client class  """


class RestClient:
  def __init__(self, config):
    self.config = config
    self._api_key = config.get("Rest", "api_key")
    self._prefix = "/api"
    self._host = config.get("Rest", "hostname")
    self._port = 5000
    self._headers = {'Content-Type': 'application/json', 'X-Api-Key': self._api_key}

  def start_job(self):
    logging.debug("Starting job")
    url = "http://" + self._host + ":" + str(self._port) + "/api/job"
    data = json.dumps({'command': 'start'})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  def pause_job(self):
    logging.debug("Pausing job")
    url = "http://" + self._host + ":" + str(self._port) + "/api/job"
    data = json.dumps({'command': 'pause'})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  def cancel_job(self):
    logging.debug("Cancelling job")
    url = "http://" + self._host + ":" + str(self._port) + "/api/job"
    data = json.dumps({'command': 'cancel'})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  def resume_job(self):
    logging.debug("Resuming job")
    url = "http://" + self._host + ":" + str(self._port) + "/api/job"
    data = json.dumps({'command': 'pause'})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  def send_gcode(self, cmd):
    logging.debug("Sending gcode")
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/command"
    data = json.dumps({'command': cmd})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  def start_preheat(self):
    logging.debug("Starting preheat")
    bed_temp = self.config.get("Preheat", "bed_temp")
    tool_0 = self.config.get("Preheat", "t0_temp")
    tool_1 = self.config.get("Preheat", "t1_temp")
    self.set_bed_temp(bed_temp)
    self.set_tool_temp(0, tool_0)
    self.set_tool_temp(1, tool_1)

  def stop_preheat(self):
    logging.debug("Stopping preheat")
    self.set_bed_temp(0)
    self.set_tool_temp(0, 0)
    self.set_tool_temp(1, 0)

  #
  def set_bed_temp(self, temp):
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/bed"
    data = json.dumps({'command': 'target', 'target': int(float(temp))})
    r = requests.post(url, data=data, headers=self._headers)
    #print (r.json)

  #
  def set_tool_temp(self, tool_nr, temp):
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/tool"
    data = json.dumps({'command': 'target', 'targets': {'tool' + str(tool_nr): int(float(temp))}})
    r = requests.post(url, data=data, headers=self._headers)
    #print (r.json)

  # Select a model
  def select_file(self, filename):
    print("Select file")
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/files/local/" + filename
    data = json.dumps({'command': 'select'})
    r = requests.post(url, data=data, headers=self._headers)
    print(r.json)

  # Jog the printer
  def jog(self, amount):
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/printhead"
    data = json.dumps({
        'command': 'jog',
        'x': amount["x"] if "x" in amount else 0,
        'y': amount["y"] if "y" in amount else 0,
        'z': amount["z"] if "z" in amount else 0
    })
    r = requests.post(url, data=data, headers=self._headers)

  # Home selected axes
  def home(self, axes):
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/printhead"
    data = json.dumps({'command': 'home', 'axes': axes})
    r = requests.post(url, data=data, headers=self._headers)

  # Extrude
  def extrude(self, amount):
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/tool"
    data = json.dumps({'command': 'extrude', 'amount': amount})
    r = requests.post(url, data=data, headers=self._headers)

  # Select Extruder E/H
  def select_tool(self, tool):
    print("selecting " + tool)
    url = "http://" + self._host + ":" + \
        str(self._port) + "/api/printer/tool"
    data = json.dumps({'command': 'select', 'tool': tool})
    r = requests.post(url, data=data, headers=self._headers)
    print(r)

  # Get list of files
  def get_list_of_files(self):
    url = "http://" + self._host + ":" + str(self._port) + "/api/files"
    data = json.dumps({})
    try:
      r = requests.get(url, params=data, headers=self._headers)
    except requests.ConnectionError as e:
      logging.warning("Connection error")
      return None
    if r.status_code in [200, 204]:
      return r.json()

    logging.warning("Unable to contact OctoPrint by REST. Check your API key (currently '" +
                    self._api_key + "'")
    return None
