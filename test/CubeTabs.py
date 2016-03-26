from gi.repository import Clutter, Mx, Cogl
import sys

class CubeTabs():

    def __init__(self, ui, num_tabs):
        self.ui = ui
        self.num_tabs = num_tabs
        self.duration = 1000
        self.tgs = [None]*4
        self.current_side = 0
        self.sides = [None]*4

        self.box = self.ui.get_object("box")

        for i in range(self.num_tabs):        
            self.sides[i] = self.ui.get_object("side"+str(i))
            btn_prev = self.ui.get_object("side"+str(i)+"-btn-prev")
            btn_prev.connect("clicked", self.btn_prev)
            btn_next = self.ui.get_object("side"+str(i)+"-btn-next")
            btn_next.connect("clicked", self.btn_next)

            t = Clutter.PropertyTransition(property_name='rotation-angle-y')
            t.set_from(i*-90)
            t.set_to(i*-90-90)
            t.add_marker("appear", 0.5)
            t.connect("marker-reached::appear", self.appear)
            t.connect("completed", self.completed)
            t.set_duration(self.duration)
            t.set_animatable(self.ui.get_object("box"))
            t.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)
            self.tgs[i] = t 

        self.tg = self.tgs[0]

        
    def btn_prev(self, btn):
        if self.tg.is_playing():
            return
        self.dis = self.sides[self.current_side]
        self.current_side = 3 if self.current_side == 0 else self.current_side-1
        self.tg = self.tgs[self.current_side]
        self.app = self.sides[self.current_side]

        self.tg.set_direction(Clutter.TimelineDirection.BACKWARD)    
        self.tg.rewind()
        self.tg.start()

    def btn_next(self, btn):
        if self.tg.is_playing():
            return
        self.dis = self.sides[self.current_side]
        self.tg = self.tgs[self.current_side]
        self.current_side = (self.current_side + 1) % 4
        self.app = self.sides[self.current_side]
        self.tg.set_direction(Clutter.TimelineDirection.FORWARD)
        self.tg.rewind()
        self.tg.start()
        
    def appear(self, one, two, three):
        self.box.set_child_at_index(self.app, 4)
        self.app.show()

    def completed(self, one):
        self.dis.hide()

if __name__ == '__main__':
    Clutter.init( sys.argv )
    style = Mx.Style.get_default ()
    ui = Clutter.Script()
    ui.load_from_file("cube-ui.json")

    _stage = ui.get_object("stage")
    _stage.set_title( "Cubic tabs" )
    tabs = CubeTabs(ui, 4)
    _stage.connect("destroy", lambda w: Clutter.main_quit() )
    _stage.show_all()
    Clutter.main()

