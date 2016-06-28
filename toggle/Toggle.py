#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
"""
The main entry point for Toggle.

Author: Elias Bakken
email: elias(at)iagent(dot)no
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
 along with Toggle.  If not, see <http://www.gnu.org/licenses/>.
"""

#import subprocess
import logging
import time
import Queue
import sys
import os

import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Mash', '0.2')
gi.require_version('Toggle', '0.5')
gi.require_version('Mx', '1.0')
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject, GLib
from threading import Thread, current_thread
from multiprocessing import JoinableQueue

from Model import Model
from Plate import Plate
from VolumeStage import VolumeStage
from ModelLoader import ModelLoader
from Printer import Printer
from CascadingConfigParser import CascadingConfigParser
from WebSocksClient import WebSocksClient
from RestClient import RestClient
from Event import Event, PushUpdate, LocalUpdate
from Message import Message
from Graph import Graph, GraphScale, GraphPlot
from TemperatureGraph import TemperatureGraph
from FilamentGraph import FilamentGraph
from CubeTabs import CubeTabs
from Splash import Splash
from Jog import Jog


# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


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
        pass #TODO: implement this

class Toggle:

    def __init__(self):
        self.version = "1.1.2"
        logging.info("Starting Toggle "+self.version)

        file_path = os.path.join("/etc/toggle","local.cfg")
        if not os.path.exists(file_path):
            logging.info(file_path + " does not exist, Creating one")
            os.mknod(file_path)
            os.chmod(file_path, 0o777)

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
        try:
            config.ui.load_from_file(config.get("System", "ui"))
        except:
            print "Error loading UI"
            import traceback
            traceback.print_exc()
        config.stage = config.ui.get_object("stage")
        config.stage.connect("destroy", self.stop)
        config.stage.connect('key-press-event', self.key_press)

        # Set up tabs
        config.tabs = CubeTabs(config.ui, 4)
        config.splash = Splash(config)
        config.splash.set_status("Starting Toggle "+self.version+"...")
        config.jog = Jog(config)
        config.temp_graph = TemperatureGraph(config)
        config.filament_graph = FilamentGraph(config)

        # Set up SockJS and REST clients
        host = config.get("Rest", "hostname")
        config.rest_client = RestClient(config)

        # Add other stuff
        config.volume_stage = VolumeStage(config)
        config.message      = Message(config)
        config.printer      = Printer(config)
        config.loader       = ModelLoader(config)
        config.plate        = Plate(config)

        config.socks_client = WebSocksClient(config, host="ws://"+host+":5000")

        config.push_updates = JoinableQueue(10)
        self.config = config
        config.plate.make_scale()
        #config.plate.add_probe_point([30,  50, 0])
        #config.plate.add_probe_point([10,  50, 1])
        #config.plate.make_scale()
        config.stage.show()

    def run(self):
        """ Start the program. Can be called from
        this file or from a start-up script."""
        # Flip and move the stage to the right location
        # This has to be done in the application, since it is a
        # fbdev app
        if self.config.get("System", "rotation") == "90":
            self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
            self.config.ui.get_object("all").set_position(480, 0)
        elif self.config.get("System", "rotation") == "270":
            self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
            self.config.ui.get_object("all").set_position(0, 800)
        elif self.config.get("System", "rotation") == "180":
            self.config.ui.get_object("all").set_pivot_point(0.5, 0.5)
            self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 180.0)

        """ Start the process """
        self.running = True
        # Start the processes
        self.p0 = Thread(target=self.loop,
                    args=(self.config.push_updates, "Push updates"))
        self.p0.start()

        self.config.socks_client.start()
        logging.info("Toggle ready")
        Clutter.main()

    # UI events needs to happen from within the
    # main thread. This was the only way I found that would do that.
    # It looks weirdm, but it works.
    def execute(self, event):
        event.execute(self.config)
        #logging.debug("Execute from "+str(current_thread()))

    def loop(self, queue, name):
        """ When a new event comes in, execute it """
        try:
            while self.running:
                try:
                    update = queue.get(block=True, timeout=1)
                except Queue.Empty:
                    continue
                # Execute any long running operations here,
                # to keep the main thread free for animations
                if update.has_thread_execution:
                    update.execute_in_thread(self.config)
                # All UI updates must be handled by the main thread.
                Clutter.threads_add_idle(0, self.execute, update)
                queue.task_done()
        except Exception:
            logging.exception("Exception in {} loop: ".format(name))


    def stop(self, w):
        logging.debug("Stopping Toggle")
        self.running = False
        self.config.socks_client.stop()
        self.p0.join()
        Clutter.main_quit()
        logging.debug("Done")

    def key_press(self, actor, event):
        ''' Key press events for quick deveopment '''
        if event.unicode_value == "f":
            if self.config.stage.get_fullscreen():
                self.config.stage.set_fullscreen(False)
            else:
                self.config.stage.set_fullscreen(True)
        elif event.unicode_value == "q":
            self.stop(None)


def main():
    t = Toggle()
    t.run()

if __name__ == '__main__':
    main()
