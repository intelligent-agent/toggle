#!/usr/bin/env python

import gi
gi.require_version('Mx', '2.0')
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, Mx

if __name__ == '__main__':
  Clutter.init()
  style = Mx.Style.get_default()
  ui = Clutter.Script()
  ui.load_from_file("ui.json")

  _stage = ui.get_object("stage")
  _stage.set_title("Test ui")
  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.show_all()
  Clutter.main()
