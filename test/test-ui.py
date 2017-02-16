from gi.repository import Clutter, Mx, Cogl, Toggle
import sys

if __name__ == '__main__':
    Clutter.init( sys.argv )
    style = Mx.Style.get_default ()
    ui = Clutter.Script()
    ui.load_from_file("ui.json")

    _stage = ui.get_object("stage")
    _stage.set_title( "Cubic tabs" )
    _stage.connect("destroy", lambda w: Clutter.main_quit() )
    _stage.show_all()
    Clutter.main()

