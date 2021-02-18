#!/usr/bin/env python3

import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter

if __name__ == '__main__':
  Clutter.init()
  ui = Clutter.Script()
  ui.load_from_file("ui-fluid-box.json")

  _stage = ui.get_object("stage")
  _stage.set_title("Test fluid ui")
  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.show()
  Clutter.main()
