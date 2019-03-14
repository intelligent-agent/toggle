# VolumeStage
import logging
from gi.repository import Clutter, Mx, Mash, Cogl


class VolumeStage(Clutter.Actor):
  def __init__(self, config):
    super(VolumeStage, self).__init__()
    self.config = config
    self.ui = config.ui
    self.p = self.ui.get_object("volume-wrapper")

    # Set up touch events linked to the viewport
    self.vp = self.ui.get_object("volume-viewport")
    self.vp.set_reactive(True)
    self.vp.connect("scroll-event", self.scroll)
    self.rotation = int(config.screen_rot)

    self.angle_max = config.getfloat("System", "angle_max")
    self.angle_min = config.getfloat("System", "angle_min")
    self.scale_max = config.getfloat("System", "scale_max")
    self.scale_min = config.getfloat("System", "scale_min")

    self.spinner = self.ui.get_object("spinner")
    self.clicked = False
    self.scale = 1.2

    cm = Cogl.Matrix()
    m = Clutter.matrix_init_from_array(cm, [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1])
    self.ui.get_object("content-flip").set_transform(m)

    zoom = Clutter.ZoomAction()
    self.vp.add_action(zoom)
    zoom.connect("zoom", self.zoom)
    zoom.connect("gesture-begin", self.zoom_begin)
    zoom.connect("gesture-end", self.zoom_end)

    pan = Clutter.PanAction()
    self.vp.add_action(pan)
    pan.connect("pan", self.pan)
    pan.connect("gesture-begin", self.pan_begin)
    pan.connect("gesture-end", self.pan_end)
    pan.connect("gesture-cancel", self.pan_cancel)

    #self.config.stage.connect("motion-event", self.motion)

    self.zoom_start = self.scale
    self.zooming = False
    self.last_x = 0
    self.last_y = 0

    self.panning = False

  def pan_begin(self, action, actor):
    self.panning = True
    self.start_x = self.p.get_rotation_angle(Clutter.RotateAxis.Y_AXIS)
    self.start_y = self.spinner.get_rotation_angle(Clutter.RotateAxis.X_AXIS)
    #print "pan begin"
    return True

  def pan_end(self, action, actor):
    self.panning = False
    #print ("pan end")

  def pan_cancel(self, action, actor):
    #print ("pan cancel")
    self.panning = False
    return False

  def pan(self, gesture, actor, other=None, stuff=None):
    #print ("pan" + str(gesture.get_motion_delta(0)))
    if self.zooming:
      return False
    (d, x, y) = gesture.get_motion_delta(0)
    if self.rotation == 0:    # Normal
      self.start_x += x
      self.start_y += y
    elif self.rotation == 90:
      self.start_x += y
      self.start_y -= x
    elif self.rotation == 180:
      self.start_x -= x
      self.start_y -= y
    elif self.rotation == 270:
      self.start_x -= y
      self.start_y += x
    self.spinner.set_rotation_angle(Clutter.RotateAxis.X_AXIS, self.start_y)
    self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, self.start_x)
    return False

  # Record the scale on the beginning of the zoom action.
  # Also, keep the zooming state, so touch is not affected
  def zoom_begin(self, action, actor):
    self.zoom_start = self.scale
    self.zooming = True
    #print ("zoom_begin")
    return True

  def zoom_end(self, action, actor):
    self.zooming = False
    #print ("zoom_end")
    return False

  def zoom(self, action, actor, focal_point, factor):
    self.scale = self.zoom_start * factor
    self.scale = max(min(self.scale, self.scale_max), self.scale_min)
    self.spinner.set_scale(self.scale, self.scale)
    self.spinner.set_scale_z(self.scale)
    #print ("zoom")
    return False

  def zoom_cancel(self, action, actor):
    print("zoom cancel")

  def scroll(self, actor, event):
    if event.direction == Clutter.ScrollDirection.DOWN:
      self.scale -= 0.1
    elif event.direction == Clutter.ScrollDirection.UP:
      self.scale += 0.1
    self.scale = max(min(self.scale, self.scale_max), self.scale_min)
    self.spinner.set_scale(self.scale, self.scale)
    self.spinner.set_scale_z(self.scale)

  def motion(self, actor, event):
    print(event.x, event.y)
    self.config.loader.model.light_point.set_x(event.x)
    self.config.loader.model.light_point.set_y(event.y)
