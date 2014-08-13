#!/usr/bin/env python2
#! -*- coding: utf-8 -*-

from gi.repository import Clutter, Mx, Mash, Toggle
Clutter.init(None)

mxDummy = Mx.Button()
plate = Toggle.Plate.new()

style = Mx.Style.get_default ();

err = style.load_from_file("/etc/toggle/style/style.css")
script = Clutter.Script()
script.load_from_file("/etc/toggle/ui.json")
stage = script.get_object("stage")
#script.connect_signals(stage)

stage.show()

# Flip and move the stage to the right location
box = script.get_object("box")
box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 0.0)
#box.set_position(0, 800)
Clutter.main()

