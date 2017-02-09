# Plate

from gi.repository import Clutter, Mx, Mash

class Settings():
    def __init__(self, config):
        self.ui = config.ui
        self.scroller = config.ui.get_object("scroll-pane")
        self.scroller.set_reactive(True)
        self.scroller.connect("scroll-event", self.on_scroll_event)
        self.y = 0

    def on_scroll_event(self, actor, event):
        if event.direction == Clutter.ScrollDirection.DOWN:
            self.y += 40
        elif event.direction == Clutter.ScrollDirection.UP:
            self.y -= 40
        elif event.direction == Clutter.ScrollDirection.SMOOTH:
            delta = Clutter.Event.get_scroll_delta(event)
            self.y += delta[1]*40

        self.y = min(150, self.y)
        self.y = max(-2000+1080-10, self.y)

        self.x, _ = self.scroller.get_position()
        self.scroller.set_position(self.x, self.y)
