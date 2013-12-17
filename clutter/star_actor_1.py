#!/usr/bin/env python

from gi.repository import Clutter, Cogl
import sys 

class StarActor(Clutter.Actor):
    def __init__(self):
        Clutter.Actor.__init__(self)

        self.set_reactive(True)

        # set default color to black
        color = Clutter.Color.from_string("#000")[1]
        self.set_color(color)

    def set_color(self, color):
        self._color = color

    def do_paint(self):
        allocation = self.get_allocation_box()
        width, height = allocation.get_size()

        color = self._color

        Cogl.Path.new()
        Cogl.set_source_color4ub(color.red, color.green, color.blue, 255)

        Cogl.Path.move_to(width * 0.5, 0)
        Cogl.Path.line_to(width, height * 0.75)
        Cogl.Path.line_to(0, height * 0.75)
        Cogl.Path.move_to(width * 0.5, height)
        Cogl.Path.line_to(0, height * 0.25)
        Cogl.Path.line_to(width, height * 0.25)
        Cogl.Path.line_to(width * 0.5, height)

        Cogl.Path.fill()

    def do_pick(self, pick_color):
        if not self.should_pick_paint():
            return

        allocation = self.get_allocation_box()
        width, height = allocation.get_size()

        Cogl.Path.new()
        Cogl.set_source_color4ub(pick_color.red, pick_color.green, pick_color.blue, pick_color.alpha)

        Cogl.Path.move_to(width * 0.5, 0)
        Cogl.Path.line_to(width, height * 0.75)
        Cogl.Path.line_to(0, height * 0.75)
        Cogl.Path.move_to(width * 0.5, height)
        Cogl.Path.line_to(0, height * 0.25)
        Cogl.Path.line_to(width, height * 0.25)
        Cogl.Path.line_to(width * 0.5, height)

        Cogl.Path.fill()


def clicked_cb(self, *args, **kwargs):
    print("click!")

if __name__ == "__main__":
    Clutter.init(sys.argv)
    stage = Clutter.Stage()

    stage.set_title("star-actor")
    stage.connect('destroy', lambda x: Clutter.main_quit() )

    star_actor = StarActor()
    star_actor.set_size(300, 300)

    color = Clutter.Color.from_string("green")[1]
    star_actor.set_color(color)

    click_action = Clutter.ClickAction()
    click_action.connect("clicked", clicked_cb)
    star_actor.add_action(click_action)

    stage.add_actor(star_actor)
    stage.show_all()

    Clutter.main()
