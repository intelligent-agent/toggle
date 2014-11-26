# Printer

import logging
import os.path

class Printer:

    def __init__(self, config):
        self.config = config
        self.pipe = config.message_listener

        # Set up print button
        btn_print = self.config.ui.get_object("btn-print")
        btn_print.connect("touch-event", self.print_model) # Touch
        btn_print.connect("button-press-event", self.print_model) # Mouse    

        self.gcode_filename = None
    
    def print_model(self, actor, action):
        filename = self.config.loader.get_model_filename()
        self.gcode_filename = filename.replace(".stl", ".gcode")
        self.run()

    def run(self):
        self.path = self.config.get("System", "model_folder")+self.gcode_filename
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

