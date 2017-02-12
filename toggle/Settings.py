# Plate

from gi.repository import Clutter, Mx, Mash
import os
import socket
import pyconnman

class Settings():
    def __init__(self, config):
        self.ui = config.ui
        self.scroller = config.ui.get_object("scroll-pane")
        self.scroller.set_reactive(True)
        self.header_y = config.ui.get_object("scroll-header").get_height()
        self.scroller.connect("scroll-event", self.on_scroll_event)
        pan = Clutter.PanAction()
        self.scroller.add_action(pan)
        pan.connect ("pan", self.pan)
        

        self.y = self.header_y
        config.tabs.set_pane_selected_callback(0, self.on_select_callback)
        self.config = config
        self.enable_sliders()
        self.setup_wifi_tab()
        self.scroller_height = self.scroller.get_height()
        self.stage_height = self.config.ui.get_object("box").get_height()

    # Mouse scrolling event
    def on_scroll_event(self, actor, event):
        if event.direction == Clutter.ScrollDirection.DOWN:
            self.y += 40
        elif event.direction == Clutter.ScrollDirection.UP:
            self.y -= 40
        elif event.direction == Clutter.ScrollDirection.SMOOTH:
            delta = Clutter.Event.get_scroll_delta(event)
            self.y += delta[1]*40
        
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
        wifi_body = self.config.ui.get_object("wifi-body")
        ssid_combo = self.config.ui.get_object("wifi-ssid")
        aps = self.config.network.get_access_points()
        
        for ap in aps:
            wifi_body.add_actor(self.make_wifi_tab(ap)) 

    def make_wifi_tab(self, ap):
        actor = Clutter.Actor()
        actor.set_size(780, 40)
        text = Clutter.Text()
        text.set_position(120, 0)
        if ap["active"]:
            text.set_text("* "+ap["name"])
        else:
            text.set_text(ap["name"])            
        text.set_font_name("Sans 16")
        actor.add_actor(text)
        
        return actor

    # Enables tap action on all setings sliders
    def enable_sliders(self):
        for box in ["network", "wifi", "slicer", "printer"]:
            header = self.config.ui.get_object(box+"-header")
            header.set_reactive(True)
            tap = Clutter.TapAction()
            header.add_action(tap)
            tap.connect("tap", self.tap)     
            
            body = self.config.ui.get_object(box+"-body")
            body.set_height(5)
            header.is_open = False  
            header.body = body
        
    # Run when the header is taped
    def tap(self, tap, actor):
        if actor.is_open:
            actor.body.set_height(5)
            actor.is_open = False
        else:
            actor.body.set_height(-1)
            actor.is_open = True
        self.scroller_height = self.scroller.get_height()
        
        
        

