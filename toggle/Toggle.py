#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
"""
The main entry point for Toggle.

Author: Elias Bakken
email: elias(dot)bakken(at)gmail(dot)com
Website: http://www.thing-printer.com
License: GNU GPL v3: http://www.gnu.org/copyleft/gpl.html

 Redeem is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Redeem is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Redeem.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject, GLib
from threading import Thread, current_thread
from multiprocessing import JoinableQueue
import Queue

import time 
from Model import Model
from Plate import Plate 
from VolumeStage import VolumeStage
from MessageListener import MessageListener
from ModelLoader import ModelLoader
from Printer import Printer
from CascadingConfigParser import CascadingConfigParser
from WebSocksClient import WebSocksClient
from RestClient import RestClient
from Event import Event
from Message import Message

from Graph import Graph, GraphScale, GraphPlot
from TemperatureGraph import TemperatureGraph

from tornado import ioloop


color_str = lambda string: Clutter.color_from_string(string)[1]  # shortcut

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

import sys

class LoggerWriter:
    def __init__(self, config, logger, level):
        self.logger = logger
        self.level = level
        self.screen_log = config.getboolean("System", "screen_debug")

    def write(self, message):
        if message != '\n':
            self.logger.log(self.level, message)
            if self.screen_log:
                self.log_to_screen(message)
                

    def log_to_screen(self, message):
        pass
        

class Toggle:    

    def __init__(self):
        logging.info("Starting Toggle 0.6.2")
        # Parse the config files. 
        config = CascadingConfigParser([
            '/etc/toggle/default.cfg',
            '/etc/toggle/printer.cfg',    
            '/etc/toggle/local.cfg'])

        # Get loglevel from the Config file
        level = config.getint('System', 'loglevel')
        if level > 0:
            logging.getLogger().setLevel(level)

        sys.stdout = LoggerWriter(config, logging, 20)
        sys.stderr = LoggerWriter(config, logging, 50)

        Clutter.init(None)

        style = Mx.Style.get_default ()
        style.load_from_file(config.get("System", "stylesheet"))

        config.ui = Clutter.Script()
        config.ui.load_from_file(config.get("System", "ui"))

        config.stage = config.ui.get_object("stage")
        config.stage.connect("destroy", self.stop)

        # Set up temperature graph
        config.temp_graph = TemperatureGraph(config)
       

        # Set up Filament sensor graph
        filament_graph = Graph(800, 480)        
        filament = config.ui.get_object("filament")
        filament.add_child(filament_graph)        

        extruders = ["E", "H", "A", "B", "C"]
        colors    = ["blue", "red", "orange", "cyan", "white"]
        config.filament_sensors = {}
        for i in range(5):
            ext = extruders[i]
            color = color_str(colors[i])
            rgb = (color.red, color.green, color.blue)
            config.filament_sensors[ext] = GraphPlot(ext, rgb, -160, 160)
            filament_graph.add_plot(config.filament_sensors[ext])                
        
        # Add a scale to the plot
        scale = GraphScale(-160, 160, [ -150, -100, -50,  0, 50, 100, 150])
        filament_graph.add_plot(scale)       
        config.filament_graph = filament_graph

        # Add other stuff
        volume_stage = VolumeStage(config)
        plate = Plate(config)
        config.message = Message(config)
        #config.message_listener = MessageListener(config)        
        config.loader = ModelLoader(config)
        config.printer = Printer(config)
        #config.ntty = Ntty(config)

        # Set up SockJS client
        host = config.get("Rest", "hostname")
        config.socks_client = WebSocksClient(config, host="ws://"+host+":5000")

        config.push_updates = JoinableQueue(10)
        # Set up REST client
        config.rest_client = RestClient(config)
        
        self.config = config 

        self.config.toggle = self

        GObject.threads_init()

        #logging.debug("execute  from "+str(current_thread()))    

        def execute(event):
            event.execute(self.config)
        

        def text_thread():
            while self.running:
                try:
                    event = config.push_updates.get(block=True, timeout=1)
                    GLib.idle_add(execute, event)
                except Queue.Empty:
                    continue
                config.push_updates.task_done()

        config.stage.show()

        self.running = True
        self.thread = Thread(target=text_thread)
        self.thread.daemon = True
        self.thread.start()

    def filter_events(self):
        pass


    def run(self):
        """ Start the program. Can be called from 
        this file or from a start-up script."""               
        box      = self.config.ui.get_object("box")
        temp     = self.config.ui.get_object("temp")
        filament = self.config.ui.get_object("filament")
        msg      = self.config.ui.get_object("msg")
        uis = [box, temp, filament, msg]
        if self.config.getboolean("System", "filter_events"):
            Clutter.Event.add_filter(self.filter_events)

        # Flip and move the stage to the right location
        # This has to be done in the application, since it is a 
        # fbdev app
        if self.config.get("System", "rotation") == "90":
            for ui in uis:
                ui.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
                ui.set_position(480, 0)
            #self.config.graph.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
        elif self.config.get("System", "rotation") == "270":
            for ui in uis:
                ui.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
                ui.set_position(0, 800)
        elif self.config.get("System", "rotation") == "180":
            for ui in uis:
                ui.set_pivot_point(0.5, 0.5)
                ui.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 180)

        """ Start the processes """
        self.running = True
        # Start the processes
        self.p0 = Thread(target=self.loop,
                    args=(self.config.push_updates, "Push updates"))
        #p0.daemon = True
        #self.p0.start()

        # Stat the Websocks client
        self.config.socks_client.start()
        
        # Signal everything ready
        logging.info("Toggle ready")

        Clutter.main()

    def loop(self, queue, name):
        """ When a new event comes in, execute it """
        try:
            while self.running:
                try:
                    update = queue.get(block=True, timeout=1)
                except Queue.Empty:
                    continue
                update.execute(self.config)
                queue.task_done()
        except Exception:
            logging.exception("Exception in {} loop: ".format(name))

    def stop(self, w):
        logging.debug("Stop")
        self.running = False
        self.thread.join()
        self.config.socks_client.stop()
        #self.running = False
        #self.p0.join()
        logging.debug("p0 joined")        
        #self.config.socks_client.disconnect()
        logging.debug("Stopping the websocks client")
        Clutter.main_quit()
        logging.debug("Quit")
            
    
        

def main():
    t = Toggle()
    t.run()

if __name__ == '__main__':
    main()


