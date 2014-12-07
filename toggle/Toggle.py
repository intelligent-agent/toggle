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
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject

from Model import Model
from Plate import Plate 
from VolumeStage import VolumeStage
from MessageListener import MessageListener
from ModelLoader import ModelLoader
from Printer import Printer
from CascadingConfigParser import CascadingConfigParser

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

import sys

class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message != '\n':
            self.logger.log(self.level, message)


class Toggle:    

    def __init__(self):
        # Parse the config files. 
        config = CascadingConfigParser(['/etc/toggle/default.cfg', '/etc/toggle/local.cfg'])

        # Get loglevel from the Config file
        level = config.getint('System', 'loglevel')
        if level > 0:
            logging.getLogger().setLevel(level)

        sys.stdout = LoggerWriter(logging, 20)
        sys.stderr = LoggerWriter(logging, 50)

        Clutter.init(None)
        
        style = Mx.Style.get_default ()
        style.load_from_file(config.get("System", "stylesheet"))

        config.ui = Clutter.Script()
        config.ui.load_from_file(config.get("System", "ui"))

        config.stage = config.ui.get_object("stage")
        config.stage.connect("destroy", self.stop)

        volume_stage = VolumeStage(config)
        plate = Plate(config)
        config.message_listener = MessageListener(config)        
        config.loader = ModelLoader(config)
        config.printer = Printer(config)

        self.config = config 

        GObject.threads_init()

        config.stage.show()

    def filter_events(self):
        pass

    def run(self):
        """ Start the program. Can be called from 
        this file or from a start-up script."""               
        self.box = self.config.ui.get_object("box")
        if self.config.getboolean("System", "filter_events"):
            Clutter.Event.add_filter(self.filter_events)

        # Flip and move the stage to the right location
        if self.config.get("System", "rotation") == "90":
            self.box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
            self.box.set_position(480, 0)
        elif self.config.get("System", "rotation") == "270":
            self.box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
            self.box.set_position(0, 800)
        elif self.config.get("System", "rotation") == "180":
            self.box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 180.0)

        Clutter.main()

    def stop(self, w):
        logging.debug("Stop")
        self.config.printer.stop_temp_loop()
        self.config.printer.stop_print_loop()
        Clutter.main_quit()
        

def main():
    t = Toggle()
    t.run()

if __name__ == '__main__':
    main()


