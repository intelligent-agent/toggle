import time
import requests, json

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
        url = "http://"+self._host+":"+str(self._port)+"/api/job"
        data = json.dumps({'command':'start'}) 
        r = requests.post(url, data, headers = self._headers)
        print r.json

    def cancel_job(self):
        logging.debug("Cancelling job")
        url = "http://"+self._host+":"+str(self._port)+"/api/job"
        data = json.dumps({'command':'cancel'}) 
        r = requests.post(url, data, headers = self._headers)
        print r.json
    

    def start_preheat(self):
        logging.debug("Starting preheat")
        bed_temp = 0
        tool_0 = 100
        tool_1 = 0
        url = "http://"+self._host+":"+str(self._port)+"/api/printer/bed"
        data = json.dumps({
            'command':'target', 
            'target': str(bed_temp)
        }) 
        r = requests.post(url, data, headers = self._headers)
        print r.json
        url = "http://"+self._host+":"+str(self._port)+"/api/printer/tool"
        data = json.dumps({
            'command':'target', 
            'targets': {
                'tool0': str(tool_0), 
                'tool1': str(tool_1)
            }
        }) 
        r = requests.post(url, data, headers = self._headers)
        print r.json

    def select_file(self, filename):
        url = "http://"+self._host+":"+str(self._port)+"/api/files/local/"+filename
        data = json.dumps({'command':'select'})
        r = requests.post(url, data, headers = self._headers)
        print r.json

if __name__ == "__main__":
    key = "934A6B7A51B34445A6A5A51DA96713A3"
    client = RestClient(key)
    client.select_file("Tension.gco")

