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
from gi.repository import Clutter, Mx, Mash, Toggle

from Model import Model
from Plate import Plate 
from VolumeStage import VolumeStage
from MessageListener import MessageListener
from ModelLoader import ModelLoader
from Printer import Printer

# TODO: Set logging level according to configuration file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

class Toggle:    

    def __init__(self):
        Clutter.init(None)
        self.style = Mx.Style.get_default ()
        self.style.load_from_file("/etc/toggle/style/style.css")

        self.ui = Clutter.Script()
        self.ui.load_from_file("/etc/toggle/ui.json")

        self.stage = self.ui.get_object("stage")
        self.stage.connect("destroy", lambda w: Clutter.main_quit() )

        self.volume_stage = VolumeStage(self.ui)
        self.plate = Plate(self.ui)

        self.volume_viewport = self.ui.get_object("volume-viewport")

        self.plate = Plate(self.ui)

        # Set up message system
        self.message_listener = MessageListener(self.ui)        

        # Make model loader
        self.loader = ModelLoader(self.ui)

        # Make printer 
        self.printer = Printer(self.message_listener)

        # Set up print button
        btn_print = self.ui.get_object("btn-print")
        btn_print.connect("touch-event", self.print_model) # Touch
        btn_print.connect("button-press-event", self.print_model) # Mouse

        self.stage.show()

    def print_model(self, actor, action):
        model = self.loader.get_model()
        #self.stl_filename = model.filename+".stl"
        #self.slicer = Slicer(self.stl_filename)
        self.printer.gcode_filename = model+".gcode"
        self.printer.run()

    def run(self):
        """ Start the program. Can be called from 
        this file or from a start-up script."""               

        # Flip and move the stage to the right location
        kernel_version = subprocess.check_output(["uname", "-r"]).strip()
        if kernel_version == "3.14.19":
            box = self.ui.get_object("box")
            box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
            box.set_position(480, 0)

        Clutter.main()

if __name__ == "__main__":
    toggle = Toggle()
    toggle.run()

