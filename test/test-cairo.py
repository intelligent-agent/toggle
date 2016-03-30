#!/usr/bin/env python
from gi.repository import Clutter, GLib
import cairo
import math


def rounded_rect(ctx, x, y, width, height, radius, line_width):
    # FIXME the line with has to be included into the calculation
    # or else the lines overlap with small radii
    line_width
    degrees = math.pi / 180.0

    ctx.new_sub_path()
    ctx.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
    ctx.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
    ctx.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)
    ctx.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
    ctx.close_path()

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class CairoActor(Clutter.Actor):
    '''a horizontal item inside a row'''

    def __init__(self):
        super(CairoActor, self).__init__()
        self.set_background_color(color('white'))
        self.set_margin_top(50)
        self.set_margin_right(50)
        self.set_margin_bottom(50)
        self.set_margin_left(50)
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.canvas.connect('draw', self.draw)
        self.line_width = 5
        self.border_radius = 50
        self.refresh_millis = 10
        self.fill_color = 0.39, 0.58, 0.93  # crimson
        self.stroke_color = 0.8, 0.27, 0  # orange red

        self.idle_resize_id = 0
        self.connect('notify::allocation', self.on_allocation)

    def on_allocation(self, *_):
        if self.idle_resize_id == 0:
            self.idle_resize_id = Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, self.refresh_millis, self.idle_resize)

    def idle_resize(self):
        self.canvas.invalidate()
        self.canvas.set_size(*self.get_size())
        self.idle_resize_id = 0

    def draw(self, canvas, ctx, width, height):
        border_radius = self.border_radius
        if width <= border_radius * 2 or height <= border_radius * 2:
            border_radius = min((width, height)) / 2

        # clear the previous frame
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.paint()

        ctx.set_operator(cairo.OPERATOR_OVER)
        rounded_rect(
            ctx,
            0 + self.line_width,
            0 + self.line_width,
            width - self.line_width * 2,
            height - self.line_width * 2,
            border_radius,
            self.line_width
        )
        ctx.set_source_rgb(*self.fill_color)
        ctx.fill_preserve()  # fill but keep the rectangle
        ctx.set_line_width(self.line_width)
        ctx.set_source_rgb(*self.stroke_color)
        ctx.stroke()


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

    cairo_actor = CairoActor()
    stage.add_child(cairo_actor)

    # bind the size of cairo_actor to the size of the stage
    cairo_actor.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

    stage.show()
    Clutter.main()
