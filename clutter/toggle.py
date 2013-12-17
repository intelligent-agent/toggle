#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
 
from gi.repository import Clutter, Cogl
import sys
 
from star_actor_1 import StarActor
 
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
 
    stage.show_all()
    Clutter.main()
