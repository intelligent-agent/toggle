#!/usr/bin/env python
#
# [SNIPPET_NAME: Clutter Custom Actor]
# [SNIPPET_CATEGORIES: Clutter]
# [SNIPPET_DESCRIPTION: Simple Clutter example showing how to create custom actor that can be easily incorporated to an stage.]
# [SNIPPET_AUTHOR: Manuel de la Pena <mandel@themacaque.com>]
# [SNIPPET_LICENSE: GPL]
# [SNIPPET_DOCS: http://www.themacaque.com/wiki/doku.php]

import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Mash', '0.2')
gi.require_version('Toggle', '0.5')
gi.require_version('Mx', '1.0')
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject

#import Clutter
#from Clutter import Cogl


class RoundedRectangle(Clutter.Actor):
  """
  Custom actor used to draw a rectangle that can have rounded corners
  """
  __gtype_name__ = 'RoundedRectangle'

  def __init__(self, width, height, arc, step, color=None, border_color=None, border_width=0):
    """
    Creates a new rounded rectangle
    """
    super(RoundedRectangle, self).__init__()
    self._width = width
    self._height = height
    self._arc = arc
    self._step = step
    if color:
      self._color = color
    else:
      self._color = Clutter.color_from_string("#000")
    if border_color:
      self._border_color = border_color
    else:
      self._border_color = Clutter.color_from_string("#000")
    self._border_width = border_width

  def do_paint(self):

    # Draw a rectangle for the clipping
    Cogl.rectangle(0, 0, self._width, self._height)
    #Cogl.path_close()
    # Start the clip
    #Cogl.clip_push_from_path()

    # set color to border color
    Cogl.set_source_color(self._border_color)
    # draw the rectangle for the border which is the same size and the
    # object
    Cogl.path_round_rectangle(0, 0, self._width, self._height, self._arc, self._step)
    Cogl.path_close()
    # color the path usign the border color
    Cogl.path_fill()
    # set the color of the filled area
    Cogl.set_source_color(self._color)
    # draw the content with is the same size minus the wirth of the border
    # finish the clip
    Cogl.path_round_rectangle(self._border_width, self._border_width,
                              self._width - self._border_width, self._height - self._border_width,
                              self._arc, self._step)
    Cogl.path_fill()
    Cogl.path_close()

    Cogl.clip_pop()

  def do_pick(self, color):
    if self.should_pick_paint() == False:
      return
    Cogl.path_round_rectangle(0, 0, self._width, self._height, self._arc, self._step)
    Cogl.path_close()
    # Start the clip
    Cogl.clip_push_from_path()
    # set color to border color
    Cogl.set_source_color(color)
    # draw the rectangle for the border which is the same size and the
    # object
    Cogl.path_round_rectangle(0, 0, self._width, self._height, self._arc, self._step)
    Cogl.path_close()
    Cogl.path_fill()
    Cogl.clip_pop()

  def get_color(self):
    return self._color

  def set_color(self, color):
    self._color = color
    self.queue_redraw()

  def get_border_width(self):
    return self._border_width

  def set_border_width(self, width):
    self._border_width = width
    self.queue_redraw()

  def get_border_color(color):
    return self._border_color

  def set_border_color(self, color):
    self._border_color = color
    self.queue_redraw()


Clutter.init(None)
stage = Clutter.Stage()
stage.set_size(400, 400)
rect = RoundedRectangle(200, 200, 5, 0.1)
rect.set_color(Clutter.color_from_string("#123"))
rect.set_border_width(5)
rect.set_position(12, 12)
stage.add_actor(rect)
#show everything in the stage
stage.show_all()
stage.connect("destroy", Clutter.main_quit)
#main Clutter loop
Clutter.main()
