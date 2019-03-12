from __future__ import print_function
from gi.repository import Clutter, Mx, Cogl
import sys


class CubeTabs():
  def __init__(self, ui, num_tabs):
    self.ui = ui
    self.num_tabs = num_tabs
    self.duration = 1000
    self.tgs = [None] * num_tabs
    self.current_side = 0
    self.sides = [None] * num_tabs
    self.selected_callbacks = [None] * num_tabs
    self.appear_callbacks = [None] * num_tabs

    self.box = self.ui.get_object("box")

    for i in range(self.num_tabs):
      self.sides[i] = self.ui.get_object("side" + str(i))
      btn_prev = self.ui.get_object("side" + str(i) + "-btn-prev")
      tap_prev = Clutter.TapAction()
      btn_prev.add_action(tap_prev)
      tap_prev.connect("tap", self.btn_prev)

      btn_next = self.ui.get_object("side" + str(i) + "-btn-next")
      tap_next = Clutter.TapAction()
      btn_next.add_action(tap_next)
      tap_next.connect("tap", self.btn_next)

      t = Clutter.PropertyTransition(property_name='rotation-angle-y')
      t.set_from(i * -90)
      t.set_to(i * -90 - 90)
      t.add_marker("appear", 0.5)
      t.connect("marker-reached::appear", self.appear)
      t.connect("completed", self.completed)
      t.set_duration(self.duration)
      t.set_animatable(self.box)
      t.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)
      self.tgs[i] = t

    btn_next = self.ui.get_object("side5-btn-next")
    tap_next = Clutter.TapAction()
    btn_next.add_action(tap_next)
    tap_next.connect("tap", self.btn_next)

    btn_next = self.ui.get_object("side5-btn-prev")
    tap_next = Clutter.TapAction()
    btn_next.add_action(tap_next)
    tap_next.connect("tap", self.btn_prev)

    self.tg = self.tgs[0]

    # Set up page 0 to page 2 transition
    self.t2 = Clutter.PropertyTransition(property_name='rotation-angle-y')
    self.t2.set_from(0)
    self.t2.set_to(180)
    self.t2.add_marker("appear", 0.5)
    self.t2.connect("marker-reached::appear", self.appear)
    self.t2.connect("completed", self.intro_completed)
    self.t2.set_duration(self.duration)
    self.t2.set_animatable(self.box)
    self.t2.set_progress_mode(Clutter.AnimationMode.EASE_IN_OUT_CUBIC)

    self.preload = Clutter.Timeline.new(500)
    self.preload.connect("completed", self.preload_complete)

  def gesture_begin(self, btn=None, other=None):
    print("begin")
    return True

  def gesture_cancel(self, btn=None, other=None):
    print("cancel")
    return True

  def gesture_progress(self, btn=None, other=None):
    print("prgress")
    return True

  def gesture_end(self, btn=None, other=None):
    print("end")
    return True

  def btn_prev(self, btn=None, other=None):
    if self.tg.is_playing():
      return
    self.dis = self.sides[self.current_side]
    self.current_side = 3 if self.current_side == 0 else self.current_side - 1
    self.tg = self.tgs[self.current_side]
    self.app = self.sides[self.current_side]
    self.app.set_opacity(1)
    self.app.show()
    self.tg.set_direction(Clutter.TimelineDirection.BACKWARD)
    self.tg.rewind()
    self.tg.start()
    # Current side has been updated, callback if set
    if self.selected_callbacks[self.current_side]:
      self.selected_callbacks[self.current_side]()

  def btn_next(self, btn=None, other=None):
    if self.tg.is_playing():
      return
    self.dis = self.sides[self.current_side]
    self.tg = self.tgs[self.current_side]
    self.current_side = (self.current_side + 1) % 4
    self.app = self.sides[self.current_side]
    self.app.set_opacity(0)
    self.app.show()
    self.tg.set_direction(Clutter.TimelineDirection.FORWARD)
    self.tg.rewind()
    self.tg.start()
    # Current side has been updated, callback if set
    if self.selected_callbacks[self.current_side]:
      self.selected_callbacks[self.current_side]()

  def appear(self, one, two, three):
    self.box.set_child_at_index(self.app, 4)
    self.app.set_opacity(255)
    # self.app.show()

  def completed(self, one):
    self.dis.hide()

  # Runs after the side 0 to 2 transition is done
  def intro_completed(self, one):
    self.ui.get_object("side5-content").hide()
    self.ui.get_object("side0-content").show()
    self.ui.get_object("side0-btn-next").show()
    self.ui.get_object("side0-btn-prev").show()
    self.dis.hide()

  # Animation to run as soon as a connection
  def to_side_2(self):
    self.current_side = 2
    self.app = self.sides[2]
    self.dis = self.sides[0]
    self.box.set_child_at_index(self.dis, 4)
    self.app.set_opacity(1)
    self.app.show()
    self.preload.start()

  # Start animation only when side two has loaded
  def preload_complete(self, something):
    self.t2.start()

  def set_pane_selected_callback(self, pane_nr, callback):
    self.selected_callbacks[pane_nr] = callback

  def add_pane_appear_callback(self, pane_nr, callback):
    self.appear_callbacks[pane_nr] = callback


if __name__ == '__main__':
  Clutter.init(sys.argv)
  style = Mx.Style.get_default()
  ui = Clutter.Script()
  ui.load_from_file("cube-ui.json")

  _stage = ui.get_object("stage")
  _stage.set_title("Cubic tabs")
  tabs = CubeTabs(ui, 4)
  _stage.connect("destroy", lambda w: Clutter.main_quit())
  _stage.show_all()
  Clutter.main()
