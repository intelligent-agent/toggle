#!/usr/bin/env python2
#! -*- coding: utf-8 -*-

from gi.repository import Clutter, Mx, Mash, Toggle
from Model import Model
from Plate import Plate 

def model_clicked(model, event):
    print "click"
    model.move_by(100, 0)

def mouse_moved(actor, event):
    print "mouse moved"

def model_load(actor, event):
    global ui
    model = Model(ui)
    volume_stage.add_child(model)


Clutter.init(None)

mxDummy = Mx.Button()
plate = Toggle.Plate.new()

style = Mx.Style.get_default ()
err = style.load_from_file("/etc/toggle/style/style.css")

ui = Clutter.Script()
ui.load_from_file("ui.json")
stage = ui.get_object("stage")
#script.connect_signals(stage)
stage.connect("destroy", lambda w: Clutter.main_quit() )

volume_stage    = ui.get_object("volume-stage")
volume_viewport = ui.get_object("volume-viewport")
btn_load        = ui.get_object("btn-load")
btn_load.connect("button-press-event", model_load)


volume_stage.set_pivot_point (0.5, 0.5)
#volume_stage.connect("button-press-event", stage_clicked)
#volume_stage.set_reactive (True)

#Set up the light
light_set = Mash.LightSet()
light_point = Mash.PointLight()
light_directional = Mash.DirectionalLight()
light_spot = Mash.SpotLight()

# Add the model the lights to the volume viewport
volume_viewport.add_child(light_point);
volume_viewport.add_child(light_directional);
volume_viewport.add_child(light_spot);

stage.show()

# Flip and move the stage to the right location
#box = script.get_object("box")
#box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
#box.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 0.0)
#box.set_position(0, 800)
Clutter.main()

