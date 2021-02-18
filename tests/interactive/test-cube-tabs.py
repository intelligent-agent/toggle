#!/usr/bin/python3

import gi
gi.require_version('Mx', '2.0')
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, Mx

from toggle.ui.CubeTabs import CubeTabs
Clutter.init()
style = Mx.Style.get_default()
ui = Clutter.Script()
ui.load_from_file("cube-ui.json")

_stage = ui.get_object("stage")
_stage.set_title("Cubic tabs")
tabs = CubeTabs(ui, 4)
_stage.connect("destroy", lambda w: Clutter.main_quit())
_stage.show()
Clutter.main()
