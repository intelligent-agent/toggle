#!/usr/bin/env python
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, GLib
import cairo
import math
import numpy as np

import threading
import time
import random

color = lambda string: Clutter.color_from_string(string)[1]    # shortcut


class Temperature():
  def __init__(self, name, color):
    self.color = color    #1.0, 0.0, 0.0
    self.name = name
    self.line_width = 3
    self.values = []
    self.times = []
    self.cutoff_time = 30 * 60    #30 minutes

  def add_point(self, time, value):
    self.values.append(value)
    self.times.append(time)
    if len(self.times) > 10:
      self.times.pop(0)
      self.values.pop(0)

  def get_start_time(self):
    if len(self.times) == 0:
      return 0
    return self.times[0]

  def get_end_time(self):
    if len(self.times) == 0:
      return 0
    return self.times[-1]

  def get_y_max(self):
    return max(self.values)

  def draw(self, ctx, width, height):
    if len(self.times) == 0:
      return
    if len(self.times) == 1:
      x_values = np.array([width / (2), width / (2)])
      y_values = height - (np.array(self.values) * (height / self.get_y_max()))
      y_values = [y_values[0], y_values[0]]
    else:
      pixel_interval = width / (len(self.times) - 1)
      x_values = np.arange(len(self.times)) * pixel_interval
      y_values = height - (np.array(self.values) * (height / self.get_y_max()))

    ctx.move_to(x_values[0], y_values[0])

    points = list(zip(x_values, y_values))

    for point in points[1:]:
      ctx.line_to(point[0], point[1])
      #print "line to "+str(point[0])+" "+str(point[1])
    ctx.set_line_width(self.line_width)
    ctx.set_source_rgb(*self.color)


class GraphActor(Clutter.Actor):
  '''a horizontal item inside a row'''

  def __init__(self):
    super(GraphActor, self).__init__()
    self.set_background_color(color('white'))
    self.set_margin_top(50)
    self.set_margin_right(50)
    self.set_margin_bottom(50)
    self.set_margin_left(50)
    self.canvas = Clutter.Canvas()
    self.set_content(self.canvas)
    self.canvas.connect('draw', self.draw)
    self.line_width = 3
    self.refresh_millis = 10

    self.temps = []

    self.idle_resize_id = 0
    self.connect('notify::allocation', self.on_allocation)

  def on_allocation(self, *_):
    print("on allocation")
    if self.idle_resize_id == 0:
      self.idle_resize_id = Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, self.refresh_millis,
                                                        self.idle_resize)

  def idle_resize(self):
    print("idle resize")
    self.canvas.set_size(*self.get_size())
    self.idle_resize_id = 0

  # Add a datapoint
  def add_temperature(self, temp):
    self.temps.append(temp)

  def refresh(self):
    #self.canvas.invalidate()
    #self.on_allocation("")
    #self.queue_draw()
    #import random
    #self.set_x(random.randint(0, 9))
    self.canvas.invalidate()
    #self.allocate_preferred_size(Clutter.AllocationFlags.ABSOLUTE_ORIGIN_CHANGED)

  def draw(self, canvas, ctx, width, height):
    # clear the previous frame
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.paint()

    ctx.set_operator(cairo.OPERATOR_OVER)
    for temp in self.temps:
      ctx.new_sub_path()
      temp.draw(ctx, width, height - 10)
      ctx.stroke()


def add_points(temp1, temp2, graph):
  for i in range(20):
    temp1.add_point(temp1.get_end_time() + 5, random.random() * 250)
    graph.refresh()
    time.sleep(0.3)


if __name__ == '__main__':

  def stage_key(element, event):
    if event.keyval == Clutter.Escape:
      clutter_quit()

  def clutter_quit(*args):
    Clutter.main_quit()

  Clutter.init([])
  stage = Clutter.Stage()
  stage.set_size(800, 500)
  stage.set_title('Clutter - Cairo content')
  stage.set_background_color(color('white'))
  #stage.set_user_resizable(True)

  # quit when the window gets closed
  stage.connect('destroy', clutter_quit)

  # close window on escape
  stage.connect('key-press-event', stage_key)

  graph = GraphActor()
  temp = Temperature("E", (1, 0, 0))
  graph.add_temperature(temp)
  graph.refresh()

  temp2 = Temperature("H", (0, 1, 0))
  graph.add_temperature(temp2)

  t = threading.Thread(target=add_points, args=(temp, temp2, graph))
  t.start()    # after 30 seconds, "hello, world" will be printed

  stage.add_child(graph)

  # bind the size of cairo_actor to the size of the stage
  graph.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

  stage.show()
  Clutter.main()
