import gi
gi.require_version('Mx', '1.0')
gi.require_version('Clutter', '1.0')

from gi.repository import Clutter, Mx
import sys

import string


def make_keyboard(ui):
  # yapf: disable
  keys = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "<<"],
          ["a", "s", "d", "f", "g", "h", "j", "k", "l", "m"],
          [" ^", "z", "x", "c", "v", "b", "n", "m", ",", ".", "^ "],
          [" 123 ", "                                        ", " }]? "]
         ]
  # yapf: enable

  for i, row in enumerate(keys):
    key_row = ui.get_object("row-" + str(i))
    for letter in row:
      key = Mx.Button()
      key.set_style_class("keyboard")
      #key.set_property("min-width", 20)
      key.set_label(letter)
      key_row.add_actor(key)


if __name__ == '__main__':
  Clutter.init(sys.argv)
  style = Mx.Style.get_default()
  ui = Clutter.Script()

  style = Mx.Style.get_default()
  style.load_from_file("keyboard.css")

  ui.load_from_file("ui-keyboard.json")

  _stage = ui.get_object("stage")
  _stage.set_title("Test virtual keyboard")
  make_keyboard(ui)

  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.show_all()
  Clutter.main()
