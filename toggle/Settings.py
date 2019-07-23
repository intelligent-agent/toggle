# Settings-page

import gi
gi.require_version('Mx', '2.0')
gi.require_version('Clutter', '1.0')
import logging
import os
from gi.repository import Clutter, Mx


class Settings():
  def __init__(self, config):
    self.ui = config.ui
    self.scroller = config.ui.get_object("scroll-pane")
    self.scroller.set_reactive(True)
    self.header_y = config.ui.get_object("scroll-header").get_height()
    self.scroller.connect("scroll-event", self.on_scroll_event)
    pan = Clutter.PanAction()
    self.scroller.add_action(pan)
    pan.connect("pan", self.finger_pan)

    self.ap_font = config.ui.get_object("wifi-ssid").get_font_description()
    self.ap_color = config.ui.get_object("wifi-ssid").get_color()
    self.ap_width = config.ui.get_object("wifi-ssid").get_width()
    self.ap_margin_left = config.ui.get_object("wifi-ssid").get_margin_left()

    self.selected_ap = None

    self.y = self.header_y
    config.tabs.set_pane_selected_callback(0, self.on_select_callback)
    self.config = config
    self.enable_sliders()
    self.scroller_height = self.scroller.get_height()
    self.stage_height = self.config.ui.get_object("box").get_height()
    self.tabs_by_path = {}
    self.ap_state = "activated"

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
  def finger_pan(self, action, actor, event):
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

  def on_select_callback(self):
    local_ip = self.config.ui.get_object("local-ip")
    local_ip.set_text(self.config.network.get_connected_ip())
    hostname = os.uname()
    local_host_name = self.config.ui.get_object("local-hostname")
    local_host_name.set_text(hostname[1])
    remote_host_name = self.config.ui.get_object("remote-hostname")
    remote_host_name.set_text(self.config.get("Server", "host"))
    slicer_layer_height = self.config.ui.get_object("slicer-layer-height")
    slicer_layer_height.set_text(self.config.get("Slicer", "layer_height"))
    slicer_print_temp = self.config.ui.get_object("slicer-print-temp")
    slicer_print_temp.set_text(self.config.get("Slicer", "print_temperature"))
    calibrate_bed_button = self.config.ui.get_object("printer-calibrate-bed")
    tap = Clutter.TapAction()
    calibrate_bed_button.add_action(tap)
    tap.connect("tap", self.calibrate_bed)
    self.setup_wifi_tab()

  def calibrate_bed(self, tap, actor):
    self.config.rest_client.send_gcode("G29")

  def setup_wifi_tab(self):
    if not self.config.network.has_wifi_capabilities():
      return
    self.config.network.ap_added_cb = self.ap_added_cb
    self.config.network.ap_removed_cb = self.ap_removed_cb
    self.config.network.ap_prop_changed_cb = self.ap_prop_changed_cb
    self.config.network.ap_state_changed_cb = self.ap_state_changed_cb
    self.add_all_aps()

  def add_all_aps(self):
    self.wifi_body = self.config.ui.get_object("wifi-body")
    self.wifi_body.remove_all_children()
    aps = self.config.network.get_access_points()
    for ap in aps:
      self.wifi_body.add_actor(self.add_wifi_tab(ap))

  def get_actor_by_path(self, path):
    if path in self.tabs_by_path:
      return self.tabs_by_path[path]
    return None

  def ap_added_cb(self, ap):
    self.wifi_body.add_actor(self.add_wifi_tab(ap))

  def ap_removed_cb(self, ap):
    child = self.get_actor_by_path(ap["object_path"])
    if child:
      self.wifi_body.remove_child(child)

  def get_bars(self, strength):
    return ("▮▯▯▯" * 25 + "▮▮▯▯" * 25 + "▮▮▮▯" * 25 + "▮▮▮▮" * 26)[strength * 4:strength * 4 + 4]

  def get_ap_state(self):
    if self.ap_state == "activated":
      return "✓"
    if self.ap_state == "disconnected":
      return ""
    return "⧗"

  def set_text(self, text, ap):
    bars = self.get_bars(int(ap["strength"]))
    active = self.get_ap_state() if ap["active"] else ""
    text.set_text("{} {} {}".format(bars, ap["name"], active))

  def ap_prop_changed_cb(self, ap):
    actor = self.get_actor_by_path(ap["object_path"])
    if actor:
      self.set_text(actor, ap)

  def ap_state_changed_cb(self, interface, state):
    self.ap_state = state

  def add_wifi_tab(self, ap):
    actor = Clutter.Text()
    actor.set_selectable(False)
    actor.set_font_description(self.ap_font)
    actor.set_color(self.ap_color)
    actor.set_width(self.ap_width)
    actor.set_margin_left(self.ap_margin_left)
    self.set_text(actor, ap)
    tap = Clutter.TapAction()
    actor.add_action(tap)
    actor.ap = ap
    tap.connect("tap", self.ap_tap)
    actor.set_reactive(True)
    self.tabs_by_path[ap["object_path"]] = actor
    return actor

  def ap_tap(self, tap, actor):
    self.selected_ap = actor.ap
    self.config.network.activate_connection(actor.ap)

  def reconnect_last_ap(self):
    self.config.network.activate_connection(self.selected_ap)

  def enable_sliders(self):
    for box in ["network", "wifi", "slicer", "printer"]:
      header = self.config.ui.get_object(box + "-header")
      header.set_reactive(True)
      tap = Clutter.TapAction()
      header.add_action(tap)
      tap.connect("tap", self.header_tap)
      body = self.config.ui.get_object(box + "-body")
      body.set_height(5)
      header.is_open = False
      header.body = body

  def header_tap(self, tap, actor):
    if actor.is_open:
      actor.body.set_height(5)
      actor.is_open = False
    else:
      actor.body.set_height(-1)
      actor.is_open = True
    self.scroller_height = self.scroller.get_height()
