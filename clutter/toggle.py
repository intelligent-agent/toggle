#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
 
from gi.repository import Clutter, Cogl
import sys
 
from star_actor_1 import StarActor



def moveLeft(actor):
    actor.set_x(20)
 
if __name__ == '__main__':
    Clutter.init(sys.argv)
 
    _script = Clutter.Script()
    _script.load_from_file("toggle.json")
    stage = _script.get_object("stage")
    _script.connect_signals(stage)
 
    
    star_actor = StarActor()
    star_actor.set_size(100, 100)

    color = Clutter.Color.from_string("#0c0")[1]
    star_actor.set_color(color)

    view = _script.get_object("3d-stage")
    view.add_actor(star_actor)
    star_actor.set_position(20, 50)

    box = _script.get_object("box")

    box.set_rotation( Clutter.RotateAxis.Z_AXIS, -90, 0, 0, 0)
    box.set_position(0, 800)

    star_actor.set_reactive(True)
    star_actor.set_easing_duration(1000)
    star_actor.set_easing_mode(Clutter.AnimationMode.LINEAR)
    star_actor.set_x(280)
    #actor.connect('button-press-event', lambda a, e: moveRight(star_actor))

    star_actor.connect('transition-stopped::x', lambda a, n, t: moveLeft(actor))

    stage.show_all()
    Clutter.main()
    #stage.ensure_redraw()
