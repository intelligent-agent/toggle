# Printer

import logging
import os.path
import threading
from gi.repository import Clutter, Mx, Mash
import time
import sys


class Printer:
  def __init__(self, config):
    self.config = config

    # Set up UI
    # Print button
    self.btn_print = self.config.ui.get_object("btn-print")
    self.btn_pause = self.config.ui.get_object("btn-pause")
    self.btn_cancel = self.config.ui.get_object("btn-cancel")

    self.btn_next = self.config.ui.get_object("btn-next")
    self.btn_prev = self.config.ui.get_object("btn-prev")

    tap_print = Clutter.TapAction()
    self.btn_print.add_action(tap_print)
    tap_print.connect("tap", self.start_print, None)

    tap_pause = Clutter.TapAction()
    self.btn_pause.add_action(tap_pause)
    tap_pause.connect("tap", self.pause_print, None)

    tap_cancel = Clutter.TapAction()
    self.btn_cancel.add_action(tap_cancel)
    tap_cancel.connect("tap", self.cancel_print, None)

    self.progress = self.config.ui.get_object("progress-bar")
    self.time_gone = self.config.ui.get_object("time-gone")
    self.time_left = self.config.ui.get_object("time-left")

    self.lbl_stat = self.config.ui.get_object("lbl-stat")
    self.lbl_model = self.config.ui.get_object("lbl-model")

    self.heartbeat = self.config.ui.get_object("heartbeat")
    self.connection = self.config.ui.get_object("connection")
    self.printing = self.config.ui.get_object("printing")
    self.paused = self.config.ui.get_object("paused")
    #self.lbl_temp   = self.config.ui.get_object("lbl-temp")

    self.flags = {
        "operational": False,
        "paused": False,
        "printing": False,
        "sdReady": False,
        "error": False,
        "ready": False,
        "closedOrError": False
    }

  def start_print(self, btn_print, action=None, stuff=None):
    """ Slices if necessary and starts the print loop """
    if self.flags["paused"]:
      self.config.rest_client.resume_job()
    elif not self.flags["printing"]:
      self.config.rest_client.start_job()

  def pause_print(self, btn_print, action=None, stuff=None):
    if self.flags["printing"]:
      self.config.rest_client.pause_job()

  def cancel_print(self, btn_print, action=None, stuff=None):
    if self.flags["printing"] or self.flags["paused"]:
      self.config.rest_client.cancel_job()

  def set_status(self, status):
    self.lbl_stat.set_text(status)

  def set_model(self, model):
    self.lbl_model.set_text(model)

  def set_printing(self, is_printing):
    if is_printing:
      self.btn_print.set_toggled(True)
      self.btn_print.set_label("Printing")
    else:
      self.btn_heat.set_toggled(False)
      self.btn_print.set_label("Print")

  def set_printing_enabled(self, enabled):
    if enabled:
      self.btn_print.set_toggled(True)
    else:
      self.btn_print.set_toggled(False)

  def set_pause_enabled(self, enabled):
    if enabled:
      self.btn_pause.set_toggled(True)
      self.btn_cancel.set_toggled(True)
    else:
      self.btn_pause.set_toggled(False)
      self.btn_cancel.set_toggled(False)

  def update_print_button(self):
    if (self.flags["operational"] and self.config.loader.model_selected
        and (not self.flags["printing"] or self.flags["paused"])):
      self.btn_print.set_toggled(True)
    else:
      self.btn_print.set_toggled(False)

  def update_pause_button(self):
    if self.flags["printing"]:
      self.btn_pause.set_toggled(True)
    else:
      self.btn_pause.set_toggled(False)

  def update_cancel_button(self):
    if self.flags["printing"] or self.flags["paused"]:
      self.btn_cancel.set_toggled(True)
    else:
      self.btn_cancel.set_toggled(False)

  def update_next_buttons(self):
    if self.flags["operational"]:
      if self.flags["printing"]:
        self.btn_next.set_toggled(True)
        self.btn_prev.set_toggled(True)
      else:
        self.btn_next.set_toggled(False)
        self.btn_prev.set_toggled(False)
    else:
      self.btn_next.set_toggled(True)
      self.btn_prev.set_toggled(True)

  # Update the current state of the printer.
  # This sets the flags shown in the bottom left corner.
  def update_printer_state(self, state):
    # logging.debug(state)
    #print self.config.loader.model_selected
    self.set_status(state["text"])
    self.flags = state["flags"]
    self.connection.set_toggled(self.flags["operational"])
    self.printing.set_toggled(self.flags["printing"])
    self.paused.set_toggled(self.flags["paused"])

    self.update_print_button()
    self.update_cancel_button()
    self.update_pause_button()
    self.update_next_buttons()

    if self.flags["sdReady"]:
      pass
    if self.flags['error']:
      pass
    if self.flags["ready"]:
      pass
    if self.flags["closedOrError"]:
      pass

  def update_progress(self, progress):
    if progress["completion"]:
      self.progress.set_progress(progress["completion"] / 100.0)
      self.config.loader.model.set_progress(progress["completion"] / 100.0)
    if progress['printTimeLeft']:
      left = self.format_time(progress['printTimeLeft'])
      self.time_left.set_text(left)
    if progress['printTime']:
      gone = self.format_time(progress['printTime'])
      self.time_gone.set_text(gone)

  def format_time(self, seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

  def start_connect_thread(self):
    pass
    # TODO

  def flash_heartbeat(self):
    self.heartbeat.set_opacity(255)
    self.heartbeat.save_easing_state()
    self.heartbeat.set_easing_duration(1000)
    self.heartbeat.set_opacity(0)
