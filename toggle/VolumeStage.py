# VolumeStage
import logging
from gi.repository import Clutter, Mx, Mash, Toggle

class VolumeStage(Clutter.Actor):

    def __init__(self, config):
        super(VolumeStage, self).__init__()
        self.config = config
        self.ui = config.ui
        self.p = self.ui.get_object("volume-wrapper")

        # Set up touch events linked to the viewport
        self.vp = self.ui.get_object("volume-viewport")
        self.vp.set_reactive(True)
        self.vp.connect("button-press-event", self.click)
        self.vp.connect("button-release-event", self.release)
        self.vp.connect("motion-event", self.move)
        self.vp.connect("touch-event", self.touch)
        self.vp.connect("scroll-event", self.scroll)

        self.rotation = config.getint("System", "rotation")

        self.angle_max = config.getfloat("System", "angle_max")
        self.angle_min = config.getfloat("System", "angle_min")
        self.scale_max = config.getfloat("System", "scale_max")
        self.scale_min = config.getfloat("System", "scale_min")

        self.spinner = self.ui.get_object("spinner")
        self.clicked = False
        self.scale = 1.2

        action = Clutter.GestureAction()
        config.stage.add_action (action);

        action.connect ("gesture-progress", self.on_gesture_update, None);
        action.connect ("gesture-begin", self.on_gesture_begin, None);
        action.connect ("gesture-end", self.on_gesture_end, None);

        self.last_x = 0
        self.last_y = 0

    def on_gesture_begin(self, gesture, actor, other):
        #print "begin ", gesture, actor, other
        return True

    def on_gesture_update(self, gesture, actor, stuff):
        #print "on update", gesture.get_n_touch_points(), gesture.get_n_current_points()
        return True

    def on_gesture_end(self, gesture, actor, stuff):
        #print "on end", gesture
        return True

    def click(self, actor, event):
        self.last_x = event.x
        self.last_y = event.y
        self.start_x = self.p.get_rotation_angle(Clutter.RotateAxis.Y_AXIS)
        self.start_y = self.spinner.get_rotation_angle(Clutter.RotateAxis.X_AXIS)
        self.clicked = True

    def release(self, actor, event):
        self.clicked = False

    def move(self, actor, event):
        if self.clicked:
            rot_x = self.start_x+(event.x-self.last_x)
            rot_y = self.start_y+(event.y-self.last_y)
            if self.rotation == 0: # Normal
                rot_y = max(min(rot_y, self.angle_max), self.angle_min)
                self.spinner.set_rotation_angle(Clutter.RotateAxis.X_AXIS, rot_y)
                self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, rot_x)
            elif self.rotation == 90: 
                rot_x = max(min(rot_x, self.angle_max), self.angle_min)
                self.spinner.set_rotation_angle(Clutter.RotateAxis.X_AXIS, rot_x)
                self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, rot_y)
            elif self.rotation == 180: #TODO: Fix this 
                rot_y = max(min(rot_y, self.angle_max), self.angle_min)
                self.spinner.set_rotation_angle(Clutter.RotateAxis.X_AXIS, rot_y)
                self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, rot_x)
            elif self.rotation == 270: #TODO: Fix this
                rot_x = max(min(rot_x, self.angle_max), self.angle_min)
                self.spinner.set_rotation_angle(Clutter.RotateAxis.X_AXIS, rot_x)
                self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, rot_y)

    def touch(self, actor, event):
        (x, y) = event.get_coords()
        event.x = x
        event.y = y
        #logging.debug(str(x)+" "+str(y))
        self.config.printer.set_temp(str(x)+" "+str(y))
        if event.type() == Clutter.EventType.TOUCH_UPDATE:
            self.move(actor, event)
        elif event.type() == Clutter.EventType.TOUCH_BEGIN:
            self.click(actor, event)
        elif event.type() == Clutter.EventType.TOUCH_END:
            self.release(actor, event)

    def scroll(self, actor, event):       
        if event.direction == Clutter.ScrollDirection.DOWN:
            self.scale -= 0.1
        elif event.direction == Clutter.ScrollDirection.UP:
            self.scale += 0.1
        self.scale = max(min(self.scale, self.scale_max), self.scale_min)
        self.spinner.set_scale(self.scale, self.scale)
        self.spinner.set_scale_z(self.scale)

