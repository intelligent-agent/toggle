# Printer

import logging
import os.path
import threading
from gi.repository import Clutter, Mx, Mash, Toggle
import time
    

import sys 

class Printer:

    def __init__(self, config):
        self.config = config
        self.pipe = config.message_listener

        # Set up UI
        self.btn_print = self.config.ui.get_object("btn-print")
        self.btn_print.connect("clicked", self.print_model)
        self.btn_heat = self.config.ui.get_object("btn-heat")
        self.btn_heat.connect("clicked", self.preheat)
        self.lbl_status = self.config.ui.get_object("lbl-stat")

        self.gcode_filename = None
        self.print_loop_running = False
        self.temp_loop_running = False

        self.start_temp_loop()

    def preheat(self, btn):
        if self.btn_heat.get_toggled():
            btn.set_label("Heating")
            for line in self.config.items("Preheat_start"):
                self.pipe.send(line[1])
        else:
            btn.set_label("Preheat")
            for line in self.config.items("Preheat_stop"):
                self.pipe.send(line[1])

    def print_model(self, btn_print):
        """ Slices if necessary and starts the print loop """
        logging.debug("print_model")
        filename = self.config.loader.get_model_filename()
        self.gcode_filename = filename.replace(".stl", ".gcode")
        self.gcode_path = self.config.get("System", "model_folder")+self.gcode_filename
        if not self.print_loop_running:
            if os.path.exists(self.gcode_path):
                self.btn_print.set_toggled(True)
                self.btn_print.set_label("Printing")
                self.start_print_loop()
            else:
                logging.warning("Tried to start printing a non existing file: "+
                    str(self.gcode_path))
        else:
            self.stop_print_loop()
            self.btn_print.set_label("Print")
            self.btn_print.set_toggled(False)

    def slice_model(self):
        pass #TODO:

    def preheat_done(self):
        self.btn_heat.set_label("Heated")

    def set_status(self, status):
        self.lbl_status.set_text(status)

    def start_print_loop(self):
        self.print_loop_running = True
        self.print_thread = threading.Thread(target=self._print_loop)
        self.print_thread.start()

    def stop_print_loop(self):
        if self.print_loop_running:
            self.print_loop_running = False
            self.print_thread.join()

    def _print_loop(self):        
        try:
            with open(self.gcode_path, "r") as f:
                for line in f:
                    if self.print_loop_running:
                        self.pipe.send(line)
            self.print_loop_running = False
            self.btn_print.set_label("Print")
        except:
            logging.error("Error in Thread"+str(sys.exc_info()[0]))


    def start_temp_loop(self):
        self.temp_loop_running = True
        self.temp_thread = threading.Thread(target=self._temp_loop)
        self.temp_thread.start()
        
    def stop_temp_loop(self):
        logging.debug("Stopping temp loop")
        self.temp_loop_running = False
        self.temp_thread.join()

    def _temp_loop(self):
        while(self.temp_loop_running):
            self.pipe.send("M105")
            time.sleep(1)

