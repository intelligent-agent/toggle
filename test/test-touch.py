#!/usr/bin/env python

import gi
import collections
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, GLib
import cairo
import math
from random import uniform

color = lambda string: Clutter.color_from_string(string)[1]    # shortcut


class CairoActor(Clutter.Actor):
  '''a horizontal item inside a row'''

  def __init__(self):
    super(CairoActor, self).__init__()
    self.set_background_color(color('white'))
    #self.set_margin_top(50)
    #self.set_margin_right(50)
    #self.set_margin_bottom(50)
    #self.set_margin_left(50)
    self.canvas = Clutter.Canvas()
    self.set_content(self.canvas)
    self.canvas.connect('draw', self.draw)
    self.line_width = 1
    self.border_radius = 50
    self.refresh_millis = 10
    self.fill_color = 0.39, 0.58, 0.93    # crimson
    self.stroke_color = []
    self.lines = []

    self.idle_resize_id = 0
    self.connect('notify::allocation', self.on_allocation)

  def on_allocation(self, *_):
    if self.idle_resize_id == 0:
      self.idle_resize_id = Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, self.refresh_millis,
                                                        self.idle_resize)

  def idle_resize(self):
    self.canvas.invalidate()
    self.canvas.set_size(*self.get_size())
    self.idle_resize_id = 0

  def draw(self, canvas, ctx, width, height):
    # clear the previous frame
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.paint()

    ctx.set_line_width(self.line_width)
    ctx.set_operator(cairo.OPERATOR_OVER)
    #print self.lines
    i = 0
    for line in self.lines:
      if len(line):
        #print "Line"
        #print line
        ctx.set_source_rgb(*self.stroke_color[i])
        i += 1
        ctx.new_sub_path()
        ctx.move_to(line[0][0], line[0][1])
        for points in line:
          ctx.line_to(points[0], points[1])
        ctx.stroke()


if __name__ == '__main__':
  Clutter.init([])
  stage = Clutter.Stage()

  stage.set_size(400, 400)
  stage.set_title('Clutter - Cairo content')
  stage.set_background_color(color('white'))
  stage.set_user_resizable(True)
  #stage.set_fullscreen(True)

  pressed = False
  events = 0
  cairo_actor = CairoActor()
  stage.add_child(cairo_actor)

  # bind the size of cairo_actor to the size of the stage
  cairo_actor.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

  timeline = Clutter.Timeline.new(1000)
  timeline.set_repeat_count(-1)
  #timeline.add_marker("start")
  timeline.start()

  def stage_key(element, event):
    if event.keyval == Clutter.Escape:
      clutter_quit()
    ''' Key press events for quick deveopment '''
    if event.unicode_value == "f":
      if stage.get_fullscreen():
        stage.set_fullscreen(False)
      else:
        stage.set_fullscreen(True)
        print("F")
    elif event.unicode_value == "q":
      Clutter.main_quit()

  def clutter_quit(*args):
    Clutter.main_quit()

  def touch_event(actor, event):
    global events
    global pressed
    events += 1
    if isinstance(event.type, collections.Callable):
      if event.type() == Clutter.EventType.TOUCH_BEGIN:
        cairo_actor.lines.append([])
        cairo_actor.stroke_color.append((uniform(0, 1), uniform(0, 1), uniform(0, 1)))
      if event.type() == Clutter.EventType.TOUCH_UPDATE:
        x, y = event.get_coords()
        cairo_actor.lines[-1].append((x, y))
    else:
      if event.type == Clutter.EventType.BUTTON_PRESS:
        cairo_actor.lines.append([])
        cairo_actor.stroke_color.append((uniform(0, 1), uniform(0, 1), uniform(0, 1)))
        pressed = True
        #print "pressed: "+str(pressed)
      if event.type == Clutter.EventType.MOTION:
        #print "pressed: "+str(pressed)
        if pressed:
          cairo_actor.lines[-1].append((event.x, event.y))
      if event.type == Clutter.EventType.BUTTON_RELEASE:
        pressed = False

  def invalidate(val):
    global events
    print(events)
    events = 0
    cairo_actor.canvas.invalidate()

  # quit when the window gets closed
  stage.connect('destroy', clutter_quit)
  stage.connect('key-press-event', stage_key)
  stage.connect("motion-event", touch_event)
  stage.connect("button-press-event", touch_event)
  stage.connect("button-release-event", touch_event)
  stage.connect("touch-event", touch_event)
  timeline.connect("completed", invalidate)

  stage.show()
  Clutter.main()
