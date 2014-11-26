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
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl

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

class Toggle:    

    def __init__(self):
        # Parse the config files. 
        config = CascadingConfigParser(['/etc/toggle/default.cfg'])

        # Get loglevel from the Config file
        level = config.getint('System', 'loglevel')
        if level > 0:
            logging.getLogger().setLevel(level)

        Clutter.init(None)
        
        style = Mx.Style.get_default ()
        style.load_from_file(config.get("System", "stylesheet"))

        config.ui = Clutter.Script()
        config.ui.load_from_file(config.get("System", "ui"))

        config.stage = config.ui.get_object("stage")
        config.stage.connect("destroy", lambda w: Clutter.main_quit() )

        volume_stage = VolumeStage(config)
        plate = Plate(config)
        config.message_listener = MessageListener(config)        
        config.loader = ModelLoader(config)
        printer = Printer(config)

        config.stage.show()


    def run(self):
        """ Start the program. Can be called from 
        this file or from a start-up script."""               

        # Flip and move the stage to the right location
        kernel_version = subprocess.check_output(["uname", "-r"]).strip()
        if kernel_version == "3.14.19":
            box = self.ui.get_object("box")
            box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
            box.set_position(480, 0)
            self.stage.add_filter(self.filter_events)

        Clutter.main()

if __name__ == "__main__":
    toggle = Toggle()
    toggle.run()

