from gi.repository import Clutter, Mx, Cogl
import sys

class CubeTabs():

    def __init__(self, ui, num_tabs):
        self.ui = ui
        self.num_tabs = num_tabs
        self.duration = 1000
        self.tgs = []

        for j in range(self.num_tabs):
            tg = Clutter.TransitionGroup()
            tg.set_duration(self.duration)
            self.tgs.append(tg)

        for i in range(self.num_tabs):
            side = self.ui.get_object("side"+str(i))
            side.set_rotation (Clutter.RotateAxis.Y_AXIS,
                              i*90,           
                              400,
                              0,
                              -400);
            #if i != 0:
            #    side.set_opacity(0)        

            for j in range(self.num_tabs):
                t = Clutter.PropertyTransition(property_name='rotation-angle-y')
                t.set_from(i*90+j*90)
                t.set_to(i*90+j*90+90)
                t.set_animatable(side)
                t.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)
                self.tgs[j].add_transition(t)
        
        for i in range(self.num_tabs):        
            btn_prev = self.ui.get_object("side"+str(i)+"-btn-prev")
            btn_prev.connect("clicked", self.prev, self.tgs[0 if i == 0 else (self.num_tabs-i)])
            btn_next = self.ui.get_object("side"+str(i)+"-btn-next")
            btn_next.connect("clicked", self.next, self.tgs[self.num_tabs-i-1])

    def next(self, btn, tg):
        tg.set_direction(Clutter.TimelineDirection.BACKWARD)    
        tg.rewind()
        tg.start()

    def prev(self, btn, tg):
        tg.set_direction(Clutter.TimelineDirection.FORWARD)
        tg.rewind()
        tg.start()



if __name__ == '__main__':
    Clutter.init( sys.argv )
    style = Mx.Style.get_default ()
    ui = Clutter.Script()
    ui.load_from_file("cube-ui.json")

    _stage = ui.get_object("stage")
    _stage.set_title( "Cubic tabs" )

    tabs = CubeTabs(ui, 4)

    Cogl.set_backface_culling_enabled (True)

    _stage.connect("destroy", lambda w: Clutter.main_quit() )

    _stage.show_all()
    Clutter.main()





#            if i == 0:
#                t = Clutter.PropertyTransition(property_name='opacity')
#                t.set_from(0)
#                t.set_to(255)
#                t.set_animatable(side)
#                t.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)
#                self.tgs[j].add_transition(t)

