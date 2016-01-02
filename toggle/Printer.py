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
        tap_print = Clutter.TapAction()
        self.btn_print.add_action(tap_print)
        tap_print.connect("tap", self.print_model, None)

        self.btn_heat = self.config.ui.get_object("btn-heat")
        self.btn_heat.connect("clicked", self.preheat)
        tap_heat = Clutter.TapAction()
        self.btn_heat.add_action(tap_heat)
        tap_heat.connect("tap", self.preheat, None)

        self.lbl_status = self.config.ui.get_object("lbl-stat")
        self.lbl_temp = self.config.ui.get_object("lbl-temp")

        self.bed_temp = 0
        self.t0_temp = 0
        self.t1_temp = 0

        self.flags = {"printing": False, "Operational": False}
        self.heating = False

    def preheat(self, btn, other=None, stuff=None):
        logging.debug("Preheat pressed")
        if self.heating:
            self.btn_heat.set_toggled(False)            
            self.config.rest_client.stop_preheat()
            self.heating = False
        else:    
            self.btn_heat.set_toggled(True)            
            self.config.rest_client.start_preheat()
            self.heating = True

    def update_preheat(self):
        if self.btn_heat.get_toggled():
            btn.set_label("Heating")
        else:
            btn.set_label("Preheat")

    def print_model(self, btn_print):
        """ Slices if necessary and starts the print loop """
        if self.flags["printing"]:
            self.config.rest_client.cancel_job()
        else:
            self.config.rest_client.start_job()

    def preheat_done(self):
        self.btn_heat.set_label("Heated")
    
    def set_status(self, status):
        self.lbl_status.set_text(status)

    def set_temp(self, temp):
        self.lbl_temp.set_text(temp)

    def update_temperatures(self, temps):
        for temp in temps:
            #logging.debug(temp)
            if "bed" in temp:
                self.bed_temp = temp["bed"]["actual"]
            if "tool0" in temp:
                self.t0_temp = temp["tool0"]["actual"]
            if "tool1" in temp:
                self.t1_temp = temp["tool1"]["actual"]
        self.set_temp("B:{} T0:{} T1:{}".format(self.bed_temp, self.t0_temp, self.t1_temp))

    def set_printing(self, is_printing):
        if is_printing:
            logging.debug("Print started, todo: diasable controls")

    def update_printer_state(self, state):
        self.set_status(state["text"])
        self.flags = state["flags"]
            
            

