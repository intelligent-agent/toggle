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

# TODO: Set logging level according to configuration file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

class Toggle:    

    def __init__(self):
        self.style = Mx.Style.get_default ()
        self.style.load_from_file("style/style.css")

        self.ui = Clutter.Script()
        self.ui.load_from_file("ui.json")

        self.stage = self.ui.get_object("stage")
        self.stage.connect("destroy", lambda w: Clutter.main_quit() )

        btn_load = self.ui.get_object("btn-load")
        btn_load.connect("button-press-event", self.load_model)

        self.volume_stage = VolumeStage(self.ui)
        self.plate = Plate(self.ui)

        self.volume_viewport = self.ui.get_object("volume-viewport")

        self.plate = Plate(self.ui)

        # Set up message system
        self.message_listener = MessageListener(self.ui)

        self.stage.show()

        self.models = []

        #self.load_model(0, 0)

    def load_model(self, actor, event):
        model = Model(self.ui)
        #self.models.append(model)

    def print_model(self):
        pass


if __name__ == "__main__":
    Clutter.init(None)
    toggle = Toggle()

    # Flip and move the stage to the right location
    kernel_version = subprocess.check_output(["uname", "-r"]).strip()
    if kernel_version == "3.14.14":
        box = toggle.ui.get_object("box")
        box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
        box.set_position(0, 800)

    Clutter.main()
