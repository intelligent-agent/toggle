#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
 
from gi.repository import Clutter, Mx, Mash, Cogl
 
from star_actor_1 import StarActor

if __name__ == '__main__':
    Clutter.init(None)

    # Load a dummy Mx Widget so that buttons can be loaded via clutterscript
    mxDummy = Mx.Button()

    _script = Clutter.Script()
    _script.load_from_file("ui.json")
    stage = _script.get_object("stage")
    _script.connect_signals(stage)

    # Load a model from file  
    model = Mash.Model.new_from_file(Mash.DataFlags.NONE, "./suzanne.ply")
    model.set_size(200, 200)

    color = Clutter.Color.from_string("#0c0")[1]

    model.set_background_color(color)
    model.set_x(100)
    model.set_y(100)

    #mat = Cogl.Material()

    view = _script.get_object("3d-stage")
    view.add_actor(model)

    stage.show()

    # Rotate the stage 
    box = _script.get_object("box")
    box.set_easing_duration(2000)
    box.set_rotation( Clutter.RotateAxis.Z_AXIS, -90, 0, 0, 0)
    box.set_position(0, 800)

    Clutter.main()
