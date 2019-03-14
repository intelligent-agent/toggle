# Plate

import logging
import os
from gi.repository import Clutter, Mx
import gi
gi.require_version('Mx', '2.0')
gi.require_version('Clutter', '1.0')

#import socket
#import pyconnman


class Settings():
  def __init__(self, config):
    self.ui = config.ui
    self.scroller = config.ui.get_object("scroll-pane")
    self.scroller.set_reactive(True)
    self.header_y = config.ui.get_object("scroll-header").get_height()
    self.scroller.connect("scroll-event", self.on_scroll_event)
    pan = Clutter.PanAction()
    self.scroller.add_action(pan)
    pan.connect("pan", self.pan)

    ok_tap = Clutter.TapAction()
    config.ui.get_object("wifi-ok").add_action(ok_tap)
    ok_tap.connect("tap", self.ok_tap)
    cancel_tap = Clutter.TapAction()
    config.ui.get_object("wifi-cancel").add_action(cancel_tap)
    cancel_tap.connect("tap", self.cancel_tap)

    self.wifi_password = ""
    self.selected_ap = None

    self.y = self.header_y
    config.tabs.set_pane_selected_callback(0, self.on_select_callback)
    self.config = config
    self.enable_sliders()
    self.setup_wifi_tab()
    self.scroller_height = self.scroller.get_height()
    self.stage_height = self.config.ui.get_object("box").get_height()
    # self.make_keyboard(0)

  # Mouse scrolling event
  def on_scroll_event(self, actor, event):
    if event.direction == Clutter.ScrollDirection.DOWN:
      self.y += 40
    elif event.direction == Clutter.ScrollDirection.UP:
      self.y -= 40
    elif event.direction == Clutter.ScrollDirection.SMOOTH:
      delta = Clutter.Event.get_scroll_delta(event)
      self.y += delta[1] * 40

    self.y = min(self.header_y, self.y)
    self.y = max(-self.scroller_height + self.stage_height, self.y)

    self.x, _ = self.scroller.get_position()
    self.scroller.set_position(self.x, self.y)

  # Finger pan action
  def pan(self, action, actor, event):
    #print action.get_motion_delta(0)
    d = action.get_motion_delta(0)
    if self.config.screen_rot == "0":
      delta = d[2]
    elif self.config.screen_rot == "90":
      delta = -d[1]
    elif self.config.screen_rot == "180":
      delta = -d[2]
    elif self.config.screen_rot == "270":
      delta = d[1]

    self.y += delta
    self.y = min(self.header_y, self.y)
    self.y = max(-self.scroller_height + self.stage_height, self.y)

    self.x, _ = self.scroller.get_position()
    self.scroller.set_position(self.x, self.y)

  # Called after the pane appears
  def on_appear_callback(self):
    pass

  # Called after the pane is chosen
  def on_select_callback(self):
    # add local IP
    local_ip = self.config.ui.get_object("local-ip")
    local_ip.set_text(self.config.network.get_connected_ip())

    # Add local hostname
    hostname = os.uname()
    local_host_name = self.config.ui.get_object("local-hostname")
    local_host_name.set_text(hostname[1])

    # Add remote address
    remote_host_name = self.config.ui.get_object("remote-hostname")
    remote_host_name.set_text(self.config.get("Rest", "hostname"))

    # Add Slicer height
    slicer_layer_height = self.config.ui.get_object("slicer-layer-height")
    slicer_layer_height.set_text(self.config.get("Slicer", "layer_height"))

    # Add Slicer print temp
    slicer_print_temp = self.config.ui.get_object("slicer-print-temp")
    slicer_print_temp.set_text(self.config.get("Slicer", "print_temperature"))

    # Add the button for calibrating the bed
    calibrate_bed_button = self.config.ui.get_object("printer-calibrate-bed")
    tap = Clutter.TapAction()
    calibrate_bed_button.add_action(tap)
    tap.connect("tap", self.calibrate_bed)

  def calibrate_bed(self, tap, actor):
    self.config.rest_client.send_gcode("G29")

  def setup_wifi_tab(self):
    if not self.config.network.has_wifi_capabilities():
      return
    wifi_body = self.config.ui.get_object("wifi-body")
    wifi_body.remove_all_children()
    ssid_combo = self.config.ui.get_object("wifi-ssid")
    self.actor_width = wifi_body.get_width()
    aps = self.config.network.get_access_points()

    for ap in aps:
      wifi_body.add_actor(self.make_wifi_tab(ap))

  def make_wifi_tab(self, ap):
    logging.debug("make_wifi")
    actor = Clutter.Actor()
    actor.set_size(self.actor_width, 40)
    text = Mx.Label()
    text.set_position(120, 0)
    if ap["active"]:
      text.set_text("* " + ap["name"])
    else:
      text.set_text(ap["name"])
    #text.set_font_name("Sans 16")
    text.set_style_class("wifi")
    actor.add_actor(text)
    tap = Clutter.TapAction()
    actor.add_action(tap)
    actor.ap = ap
    tap.connect("tap", self.ap_tap)
    actor.set_reactive(True)

    return actor

  # Called when a wifi network is tapped
  def ap_tap(self, tap, actor):
    if self.config.network.ap_needs_password(actor.ap):
      self.wifi_password = ""
      self.selected_ap = actor.ap
      self.config.ui.get_object("wifi-input").set_text(self.wifi_password)
      self.set_wifi_status("For " + self.selected_ap["name"])
      self.make_keyboard(0)
    else:
      self.config.network.activate_connection(actor.ap)
      self.setup_wifi_tab()
    print("AP-tap")

  # Called when OK in the wifi screen is taped
  def ok_tap(self, tap, actor):
    self.wifi_password = self.config.ui.get_object("wifi-input").get_text()
    self.set_wifi_status("Connecting to " + self.selected_ap["name"])
    result = self.config.network.update_password(self.selected_ap, self.wifi_password)
    result = self.config.network.activate_connection(self.selected_ap)
    if result == "OK":
      self.set_wifi_status("Connected")
      self.config.ui.get_object("wifi-overlay").hide()
    else:
      self.set_wifi_status("Unable to connect")

  def set_wifi_status(self, text):
    self.config.ui.get_object("wifi-status").set_text(text)

  # Called when Cancel is tapped
  def cancel_tap(self, tap, actor):
    self.config.ui.get_object("wifi-overlay").hide()

  # Enables tap action on all setings sliders
  def enable_sliders(self):
    for box in ["network", "wifi", "slicer", "printer"]:
      header = self.config.ui.get_object(box + "-header")
      header.set_reactive(True)
      tap = Clutter.TapAction()
      header.add_action(tap)
      tap.connect("tap", self.tap)
      body = self.config.ui.get_object(box + "-body")
      body.set_height(5)
      header.is_open = False
      header.body = body

  # Run when the header is tapped
  def tap(self, tap, actor):
    if actor.is_open:
      actor.body.set_height(5)
      actor.is_open = False
    else:
      actor.body.set_height(-1)
      actor.is_open = True
    self.scroller_height = self.scroller.get_height()

  def keyboard_tap(self, tap, actor):
    self.wifi_password = self.config.ui.get_object("wifi-input").get_text()
    if actor.letter == " << ":
      self.wifi_password = self.wifi_password[:-1]
    elif actor.letter == "                                        ":
      self.wifi_password += " "
    elif actor.letter == "                                        ":
      self.wifi_password += " "
    elif actor.letter == " 123 " or actor.letter == " }]? ":
      self.make_keyboard(1)
    elif actor.letter == " ^":
      self.make_keyboard(2)
    elif actor.letter == "^ " or actor.letter == " ABC ":
      self.make_keyboard(0)
    else:
      self.wifi_password += actor.letter
    self.config.ui.get_object("wifi-input").set_text(self.wifi_password)

  def make_keyboard(self, keyset=0):
    # yapf: disable
    keys = [[["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", " << "],
             ["a", "s", "d", "f", "g", "h", "j", "k", "l", "'"],
             [" ^", "z", "x", "c", "v", "b", "n", "m", ",", ".", " ^"],
             [" 123 ", "                                        ", " }]? "]
             ],
            [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " << "],
             ["=", "-", "+", "*", "/", "\\", ":", ";", "'", "\""],
             ["(", ")", "#", "$", "!", "?", "@", "m", ",", "."],
             [" ABC ", "                                        ", " ABC "]
             ],
            [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", " << "],
             ["A", "S", "D", "F", "G", "H", "J", "K", "L", "'"],
             ["^ ", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "^ "],
             [" 123 ", "                                        ", " }]? "]
             ]]
    # yapf: enable

    for i, row in enumerate(keys[keyset]):
      key_row = self.config.ui.get_object("row-" + str(i))
      key_row.remove_all_children()
      for letter in row:
        key = Mx.Button()
        key.set_style_class("keyboard")
        key.set_label(letter)
        key.letter = letter
        key_row.add_actor(key)
        tap = Clutter.TapAction()
        key.add_action(tap)
        tap.connect("tap", self.keyboard_tap)

    self.config.ui.get_object("wifi-overlay").show()
