from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject, GLib
import sys

state = 0

def keyPress(self, event, tgs):
    print "keypress"
    global state
    tgs[state].start()
    state += 1
    if state >= 4:
        state = 0
    #Clutter.State.set_state(_transitions, "side0")
    #transition.start()


def change_side(btn, tgs, direction):
    tgs.set_direction(direction)    
    tgs.rewind ()
    tgs.start()

if __name__ == '__main__':
    Clutter.init( sys.argv )


    style = Mx.Style.get_default ()


    ui = Clutter.Script()
    ui.load_from_file("cube-ui.json")

    _stage = ui.get_object("stage")
    _stage.set_title( "Cubic tabs" )

    

    #ui.connect_signals(_stage)

    #transitions = Clutter.State()

    tgs = []

    for j in range(4):
        tg = Clutter.TransitionGroup()
        tg.set_duration(1000)
        tgs.append(tg)

    for i in range(4):
        side = ui.get_object("side"+str(i))
        side.set_rotation (Clutter.RotateAxis.Y_AXIS,
                          i*90,           
                          400,
                          0,
                          -400);

        for j in range(4):
            transition = Clutter.PropertyTransition(property_name='rotation-angle-y')
            transition.set_from(i*90+j*90)
            transition.set_to(i*90+j*90+90)
            transition.set_animatable(side)
            transition.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)
            tgs[j].add_transition(transition)
        

    btn_prev = ui.get_object("side0-btn-prev")
    btn_prev.connect("clicked", change_side, tgs[0], Clutter.TimelineDirection.FORWARD)
    btn_next = ui.get_object("side0-btn-next")
    btn_next.connect("clicked", change_side, tgs[3], Clutter.TimelineDirection.BACKWARD)

    btn_prev = ui.get_object("side1-btn-prev")
    btn_prev.connect("clicked", change_side, tgs[3], Clutter.TimelineDirection.FORWARD)
    btn_next = ui.get_object("side1-btn-next")
    btn_next.connect("clicked", change_side, tgs[2], Clutter.TimelineDirection.BACKWARD)

    btn_prev = ui.get_object("side2-btn-prev")
    btn_prev.connect("clicked", change_side, tgs[2], Clutter.TimelineDirection.FORWARD)
    btn_next = ui.get_object("side2-btn-next")
    btn_next.connect("clicked", change_side, tgs[1], Clutter.TimelineDirection.BACKWARD)

    btn_prev = ui.get_object("side3-btn-prev")
    btn_prev.connect("clicked", change_side, tgs[1], Clutter.TimelineDirection.FORWARD)
    btn_next = ui.get_object("side3-btn-next")
    btn_next.connect("clicked", change_side, tgs[0], Clutter.TimelineDirection.BACKWARD)

    Cogl.set_backface_culling_enabled (True)

    _stage.connect("destroy", lambda w: Clutter.main_quit() )
    #_stage.connect('key-press-event', keyPress, tgs)
    _stage.show_all()
    Clutter.main()
