from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject, GLib

if __name__ == '__main__':

  Clutter.init([])
  stage = Clutter.Stage()
  stage.set_size(800, 480)
  stage.set_title('Clutter - Load image')
  stage.set_user_resizable(True)

  stage.set_layout_manager(Clutter.BinLayout())

  splash = Clutter.Texture.new_from_file("Toggle_splash.png")
  stage.add_child(splash)

  # quit when the window gets closed
  stage.connect("destroy", lambda w: Clutter.main_quit())

  stage.show()
  Clutter.main()
