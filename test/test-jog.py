from gi.repository import Clutter, Mx, Cogl
import sys


class Jog:
  def __init__(self, config=None):
    self.config = config

    buttons = [
        "jog_x_minus", "jog_x_plus", "jog_y_minus", "jog_y_plus", "jog_z_minus", "jog_z_plus",
        "jog_home", "jog_z_home", "jog_e_extrude", "jog_e_retract", "jog_e_toggle"
    ]

    for name in buttons:
      print(name)
      if hasattr(self, name):
        btn = config.ui.get_object(name)
        func = getattr(self, name)
        tap = Clutter.TapAction()
        btn.add_action(tap)
        tap.connect("tap", func, None)
      else:
        print("missing function " + str(name))

  def jog_x_minus(self, btn, etc=None, other=None):
    print("jog x min")

  def jog_x_plus(self, btn, etc=None, other=None):
    print("jog x plus")

  def jog_y_minus(self, btn, etc=None, other=None):
    print("jog y min")

  def jog_y_plus(self, btn, etc=None, other=None):
    print("jog y plus")

  def jog_home(self, btn, etc=None, other=None):
    print("jog home")

  def jog_z_plus(self, btn, etc=None, other=None):
    print("jog z plus")

  def jog_z_minus(self, btn, etc=None, other=None):
    print("jog z minus")

  def jog_z_home(self, btn, etc=None, other=None):
    print("jog home z")

  def jog_e_extrude(self, btn, etc=None, other=None):
    print("extrude")

  def jog_e_retract(self, btn, etc=None, other=None):
    print("retract")

  def jog_e_toggle(self, btn, etc=None, other=None):
    print("Toggle e")


if __name__ == '__main__':
  Clutter.init(sys.argv)

  style = Mx.Style.get_default()
  style.load_from_file("style/style.css")

  ui = Clutter.Script()
  ui.load_from_file("jog-ui.json")

  class Config:
    pass

  config = Config()
  config.ui = ui

  Jog(config)

  _stage = ui.get_object("stage")
  _stage.set_title("Jog UI")
  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.show_all()
  Clutter.main()
