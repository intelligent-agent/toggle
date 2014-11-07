# Printer

import logging
import os.path

class Printer:

    def __init__(self, pipe):
        self.pipe = pipe    
        self.gcode_filename = None
    
    def run(self):
        self.path = "/usr/share/models/"+self.gcode_filename
        if os.path.exists(self.path):
            self.running = True
            self.thread = threading.Thread(target=_loop)
        else:
            logging.warning("Tried to start printing a non existing file: "+
                str(self.path))

    def stop(self):
        self.running = False
        self.thread.join()

    def _loop(self):
        with open(self.gcode_filename) as f:
            for line in f:
                if self.running:
                    self.pipe.send(line)

