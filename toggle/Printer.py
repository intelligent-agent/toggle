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

        self.bed_temp = 0
        self.t0_temp = 0
        self.t1_temp = 0

    def preheat(self, btn):
        logging.debug("Preheat pressed")
        self.config.rest_client.start_preheat()

    def update_preheat(self):
        if self.btn_heat.get_toggled():
            btn.set_label("Heating")
        else:
            btn.set_label("Preheat")

    def print_model(self, btn_print):
        """ Slices if necessary and starts the print loop """
        self.config.rest_client.start_print()

    def set_print_status(self):
        #self.btn_print.set_toggled(True)
        #self.btn_print.set_label("Printing")
        #self.btn_print.set_label("Print")
        #self.btn_print.set_toggled(False)
        pass


    def preheat_done(self):
        self.btn_heat.set_label("Heated")
    
    def set_status(self, status):
        self.lbl_status.set_text(status)

    def update_temperatures(self, temps):
        for temp in temps:
            logging.debug(temp)
            if "bed" in temp:
                self.bed_temp = temp["bed"]["actual"]
            if "tool0" in temp:
                self.t0_temp = temp["tool0"]["actual"]
            if "tool1" in temp:
                self.t1_temp = temp["tool1"]["actual"]
        self.set_status("B:{} T0:{} T1:{}".format(self.bed_temp, self.t0_temp, self.t1_temp))

    def set_printing(self, is_printing):
        if is_printing:
            logging.debug("Print started, todo: diasable controls")

    def update_printer_state(self, state):
        if "flags" in state:
            self.operational = state["flags"]["operational"]
            self.printing    = state["flags"]["printing"]

        

