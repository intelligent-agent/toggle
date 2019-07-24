#!/usr/bin/env python3
# Temp graph
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, GLib
import cairo
import math
import threading
import time

import logging


class GraphPlot():
  def __init__(self, name, color, scale_min=0.0, scale_max=320.0):
    self.color = color
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
  def __init__(self, color, scale_min, scale_max, lines):
    self.scale_max = float(scale_max)
    self.scale_min = float(scale_min)
    self.scale_tot = float(abs(scale_max - scale_min))
    self.y_values = lines
    self.x_values = []
    self.color = color
    self.line_width = 1

  def line_y_pos(self, height, y):
    return height - (y - self.scale_min) * (height / self.scale_tot)

  def draw(self, ctx, width, height):
    ctx.set_line_width(self.line_width)
    ctx.set_source_rgba(*self.color)
    for y in self.y_values:
      line_y = self.line_y_pos(height, y)
      ctx.move_to(23, line_y)
      ctx.line_to(width, line_y)
      ctx.move_to(0, line_y)
      ctx.show_text(str(y))


class Graph(Clutter.Actor):
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
