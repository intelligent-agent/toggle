
import logging
import os
import time

from gi.repository import GLib

from threading import current_thread

class PushUpdate:

    def __init__(self, update_type, payload):
        self.update_type = update_type
        self.payload = payload

    def execute(self, config):
        self.config = config
        if hasattr(self, self.update_type):
            #logging.debug("Got PushUpdate "+self.update_type+" "+str(current_thread()))
            getattr(self, self.update_type)()
        else:
            print "missing function "+str(self.update_type)

    def connected(self):
        self.config.connected = self.payload

    def history(self):
        temps = self.payload["temps"]
        for temp in temps:
            time = temp["time"]
            tool_0 = temp["tool0"]["actual"]
            tool_1 = temp["tool1"]["actual"]
            bed    = temp["bed"]["actual"]
            self.config.temp_e.add_point(time, tool_0)
            self.config.temp_h.add_point(time, tool_1)
            self.config.temp_bed.add_point(time, bed)

    def timelapse(self):
        pass

    def plugin(self):
        #print "Plugin!"
        #print self.payload
        plugin_type = self.payload["data"]["type"]
        plugin_data = self.payload["data"]["data"]
        plugin_name = self.payload["plugin"]
        if plugin_type == "filament_sensor":
            #logging.debug("filament sensor data")
            message = plugin_data["message"]
            time    = int(plugin_data["time"])
            [filament_name, filament_value] = message.split(":")
            if filament_name in self.config.filament_sensors:
                sensor = self.config.filament_sensors[filament_name]
                sensor.add_point(time, float(filament_value)) 
                self.config.filament_graph.refresh()
            else:
                logging.info("Unknown extruder: "+str(filament_name))
        elif plugin_type == "alarm_filament_jam":
            self.config.message.display("Alarm: Filament Jam!") 
        elif plugin_type == "display_message":
            message = plugin_data["message"]
            self.config.message.display(message) 
        else:
            logging.debug("Unknown plugin type: "+str(plugin_type))


    def current(self):
        self.config.state = self.payload
        self.config.printer.update_printer_state(self.payload["state"])
        self.config.printer.update_temperatures(self.payload["temps"])

    def event(self):
        evt_type = self.payload["type"]
        payload = self.payload["payload"]
        e = Event(self.config, evt_type, payload)

    def slicingProgress(self):
        prog = self.payload["progress"]
        self.config.message.display("Slicing progress: {}%".format(prog))

    def state(self):
        print "Got state!"



class Event:

    def __init__(self, config, evt_type, payload):
        self.config = config
        self.payload = payload
        #print "Got event"
        if hasattr(self, evt_type):
            getattr(self, evt_type)()
        else:
            print "missing event function "+str(evt_type)

    def FileSelected(self):
        filename = os.path.splitext(self.payload["filename"])[0]+".stl"
        self.config.loader.select_model(filename)

    def FileDeselected(self):
        logging.debug("Deselected "+self.payload["filename"])
        filename = os.path.splitext(self.payload["filename"])[0]+".stl"
        #config.loader.select_model(filename)

    def UpdatedFiles(self):
        logging.debug("Updated files")

    def Upload(self):
        logging.debug("Upload evt")
        config.loader.load_models()

    def Disconnected(self):
        logging.debug("Printer Disconnected")

    def Connected(self):
        logging.debug("Printer Connected")
            
    def ClientOpened(self):
        logging.debug("Client Opened")

    def ClientClosed(self):
        logging.debug("Client Closed")

    def SlicingStarted(self):
        print self.payload
        self.config.message.display("Starting slicing!")
        
    def SlicingDone(self):
        print self.payload
        self.config.message.display("Slicing done!")
        
        
