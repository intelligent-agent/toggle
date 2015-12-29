
import logging
import os

class Event:

    def __init__(self, evt_type, payload):
        self.evt_type = evt_type
        self.payload = payload    

    def execute(self, config):
        logging.info("Executing event "+str(self.evt_type))
        if self.evt_type == "FileSelected":
            filename = os.path.splitext(self.payload["filename"])[0]+".stl"
            config.loader.select_model(filename)
                    

