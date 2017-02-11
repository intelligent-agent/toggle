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
        self.scroller.connect("scroll-event", self.on_scroll_event)
        self.y = 0
        config.tabs.set_pane_selected_callback(0, self.on_select_callback)
        self.config = config
        self.enable_sliders()

    # Mouse scrolling event
    def on_scroll_event(self, actor, event):
        if event.direction == Clutter.ScrollDirection.DOWN:
            self.y += 40
        elif event.direction == Clutter.ScrollDirection.UP:
            self.y -= 40
        elif event.direction == Clutter.ScrollDirection.SMOOTH:
            delta = Clutter.Event.get_scroll_delta(event)
            self.y += delta[1]*40

        self.y = min(150, self.y)
        self.y = max(-2000+1080-10, self.y)

        self.x, _ = self.scroller.get_position()
        self.scroller.set_position(self.x, self.y)


    # Called after the pane appears
    def on_appear_callback(self):
        pass

    # Called after the pane is chosen
    def on_select_callback(self):
        # add local IP
        local_ip = self.config.ui.get_object("local-ip")
        ip_addr = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        local_ip.set_text(ip_addr)

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


    # Enables tap action on all setings sliders
    def enable_sliders(self):
        for box in ["network", "wifi", "slicer", "printer"]:
            header = self.config.ui.get_object(box+"-header")
            header.set_reactive(True)
            tap = Clutter.TapAction()
            header.add_action(tap)
            tap.connect("tap", self.tap)     
            
            body = self.config.ui.get_object(box+"-body")
            header.is_open = False  
            header.body = body
        

    # Run when teh header is taped
    def tap(self, tap, actor):
        if actor.is_open:
            actor.body.set_height(5)
            actor.is_open = False
        else:
            actor.body.set_height(300)
            actor.is_open = True

        

