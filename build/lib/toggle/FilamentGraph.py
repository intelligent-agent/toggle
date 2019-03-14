from .Graph import Graph, GraphScale, GraphPlot

from gi.repository import Clutter, Mx, Mash

import logging


def color_str(string):
  return Clutter.color_from_string(string)[1]    # shortcut


class FilamentGraph():
  def __init__(self, config):
    self.config = config

    # Set up filament graph
    self.graph = Graph(800, 380)
    self.filament = config.ui.get_object("graph")
    self.filament.add_child(self.graph)
    self.graph.hide()

    tap = Clutter.TapAction()
    self.graph.add_action(tap)
    tap.connect("tap", self.change_to_temperature)
    self.graph.set_reactive(True)

    self.graphs = {
        "E": {
            "actual": GraphPlot("E", (1, 0, 0), -165, 165)
        },
        "H": {
            "actual": GraphPlot("H", (1, 0.64, 0), -165, 165)
        },
        "A": {
            "actual": GraphPlot("A", (0, 0, 1), -165, 165)
        }
    }

    for tool in self.graphs:
      for source in self.graphs[tool]:
        # logging.debug(self.graphs[tool][source])
        self.graph.add_plot(self.graphs[tool][source])

    # Add a scale to the plot
    scale = GraphScale(-165, 165, [-150, -100, -50, 0, 50, 100, 150])
    scale.set_title("Filament")
    self.graph.add_plot(scale)

  def update_filaments(self, message):
    time = int(message['time'])
    msg = message['message']
    [tool_name, tool_value] = msg.split(":")
    if tool_name in self.graphs:
      plot = self.graphs[tool_name]["actual"]
      plot.add_point(time, float(tool_value))
    else:
      logging.warning("Missing extruder name: " + str(tool_name))
    self.graph.refresh()

  def change_to_temperature(self, button, action):
    print("Tap filament")
    self.graph.hide()
    self.config.temp_graph.graph.show()
