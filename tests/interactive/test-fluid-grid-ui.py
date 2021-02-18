#!/usr/bin/env python3

import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter

sizes = [(800, 480), (1280, 720), (1920, 1080)]
index = 0

if __name__ == '__main__':
  Clutter.init()
  ui = Clutter.Script()
  ui.load_from_file("ui-fluid-grid.json")

  def key_press(actor, event):
    global index
    ''' Key press events for quick deveopment '''
    if event.unicode_value == "f":
      if _stage.get_fullscreen():
        _stage.set_fullscreen(False)
      else:
        _stage.set_fullscreen(True)
    elif event.unicode_value == "q":
      Clutter.main_quit()
    elif event.unicode_value == "r":
      _stage.set_size(sizes[index][0], sizes[index][1])
      index = (index + 1) % 3

  _stage = ui.get_object("stage")
  _stage.set_title("Test fluid ui")
  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.connect('key-press-event', key_press)

  _stage.show()
  Clutter.main()
