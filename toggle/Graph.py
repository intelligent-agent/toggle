#!/usr/bin/env python3
# Temp graph

#from gi.repository import Clutter, Mx, Mash, Toggle

from gi.repository import Clutter, GLib
import cairo
import math
import numpy as np

import threading
import time
import random
import logging


def color(string):
  return Clutter.color_from_string(string)[1]    # shortcut


class GraphPlot():
  def __init__(self, name, color, scale_min=0.0, scale_max=320.0):
    self.color = color    # 1.0, 0.0, 0.0
    self.name = name
    self.line_width = 3
    self.values = []
    self.times = []
    self.cutoff_time = 30 * 60    # 30 minutes
    self.scale_max = float(scale_max)
    self.scale_min = float(scale_min)
    self.scale_tot = float(abs(scale_max - scale_min))

  def add_point(self, time, value):
    if value is None:
      value = 0.0
    self.values.append(value)
    self.times.append(time)
    if len(self.times) > 30 * 60 / 5:
      self.times.pop(0)
      self.values.pop(0)

    #logging.debug("add_point: "+str(time)+" "+str(value))

  def draw(self, ctx, width, height):
    width -= 23
    if len(self.times) == 0:
      return
    if len(self.times) == 1:
      x_values = np.array([0, width])
      y_values = height - (np.array(self.values) - self.scale_min) * (height / self.scale_tot)
      y_values = [y_values[0], y_values[0]]
    else:
      pixel_interval = width / float(len(self.times) - 1)
      x_values = np.arange(len(self.times)) * pixel_interval + 23
      y_values = height - (np.array(self.values) - self.scale_min) * (height / self.scale_tot)

    ctx.set_line_width(self.line_width)
    ctx.set_source_rgb(*self.color)

    ctx.move_to(x_values[0], y_values[0])
    points = zip(x_values, y_values)
    for point in list(points)[1:]:
      ctx.line_to(point[0], point[1])


class GraphScale():
  def __init__(self, scale_min, scale_max, lines):
    self.scale_max = float(scale_max)
    self.scale_min = float(scale_min)
    self.scale_tot = float(abs(scale_max - scale_min))
    self.y_values = lines
    self.x_values = []
    self.color = (0, 0, 0, 128)
    self.line_width = 1
    self.title = None

  def set_title(self, title):
    self.title = title

  def draw(self, ctx, width, height):
    ctx.set_line_width(self.line_width)
    ctx.set_source_rgba(*self.color)
    for y in self.y_values:
      ctx.move_to(23, height - (y - self.scale_min) * (height / self.scale_tot))
      ctx.line_to(width, height - (y - self.scale_min) * (height / self.scale_tot))
      ctx.move_to(0, height - (y - self.scale_min) * (height / self.scale_tot))
      ctx.show_text(str(y))
    if self.title:
      ctx.move_to(width / 2.0 - 40, 16)
      ctx.set_font_size(16)
      ctx.show_text(str(self.title))


class Graph(Clutter.Actor):
  '''a horizontal item inside a row'''

  def __init__(self, width, height):
    super(Graph, self).__init__()
    self.set_size(width, height)
    self.set_margin_top(0)
    self.set_margin_right(0)
    self.set_margin_bottom(0)
    self.set_margin_left(0)
    self.canvas = Clutter.Canvas()
    self.set_content(self.canvas)
    self.canvas.connect('draw', self.draw)
    self.line_width = 3
    self.refresh_millis = 100

    self.plots = []

    self.idle_resize_id = 0
    self.connect('notify::allocation', self.on_allocation)
    self.set_reactive(True)

  def on_allocation(self, *_):
    if self.idle_resize_id == 0:
      self.idle_resize_id = Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, self.refresh_millis,
                                                        self.idle_resize)

  def idle_resize(self):
    self.canvas.invalidate()
    self.canvas.set_size(*self.get_size())
    self.idle_resize_id = 0

  # Add a datapoint
  def add_plot(self, plot):
    self.plots.append(plot)

  def refresh(self):
    self.on_allocation("")

  def draw(self, canvas, ctx, width, height):
    # clear the previous frame
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.paint()

    ctx.set_operator(cairo.OPERATOR_OVER)
    for plot in self.plots:
      ctx.new_sub_path()
      plot.draw(ctx, width, height - 10)
      ctx.stroke()


def add_points(temp1, temp2, graph):
  for i in range(20):
    temp1.add_point(temp1.get_end_time() + 5, random.random() * 200 - 100)
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
  stage.set_user_resizable(True)

  # quit when the window gets closed
  stage.connect('destroy', clutter_quit)

  # close window on escape
  stage.connect('key-press-event', stage_key)

  graph = Graph(800, 500)
  temp = GraphPlot("E", (1, 0, 0), -100, 100)
  graph.add_plot(temp)
  graph.refresh()

  temp2 = GraphPlot("H", (0, 1, 0))
  graph.add_plot(temp2)

  scale = GraphScale(-110, 110, [-100, -50, 0, 50, 100])
  graph.add_plot(scale)

  t = threading.Thread(target=add_points, args=(temp, temp2, graph))
  t.start()    # after 30 seconds, "hello, world" will be printed

  stage.add_child(graph)

  # bind the size of cairo_actor to the size of the stage
  graph.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

  stage.show()
  Clutter.main()
