from .Graph import Graph, GraphScale, GraphPlot
from gi.repository import Clutter
import logging


class TemperaturePage():
  def __init__(self, config):
    self.config = config
    self.temp = config.ui.get_object("graph")
    tc = config.ui.get_object("graph-title").get_color()
    self.graph_color = (tc.red, tc.green, tc.blue, tc.alpha)
    self.graph = Graph(self.temp.get_width(), self.temp.get_height())
    self.temp.add_child(self.graph)
    self.temps = {
        "tool0": {
            "g_actual": GraphPlot("E", (1, 0, 0)),
            "g_target": GraphPlot("T_E", (1, 0.4, 0.4)),
            "t_actual": 0,
            "t_target": 0,
            "t_preheat": 220,
            "heating": False,
            "state": "cold",
            "btn-name": "heat-tool0",
            "func-name": self.on_preheat_tool0,
            "btn": None
        },
        "tool1": {
            "g_actual": GraphPlot("H", (1, 0.64, 0)),
            "g_target": GraphPlot("T_H", (1, 0.8, 0.5)),
            "t_actual": 0,
            "t_target": 0,
            "t_preheat": 220,
            "heating": False,
            "state": "cold",
            "btn-name": "heat-tool1",
            "func-name": self.on_preheat_tool1,
            "btn": None
        },
        "tool2": {
            "g_actual": GraphPlot("A", (1, 0.64, 0)),
            "g_target": GraphPlot("T_A", (1, 0.8, 0.5)),
            "t_actual": 0,
            "t_target": 0,
            "t_preheat": 220,
            "heating": False,
            "state": "cold",
            "btn-name": "heat-tool2",
            "func-name": self.on_preheat_tool2,
            "btn": None
        },
        "bed": {
            "g_actual": GraphPlot("BED", (0, 0, 1)),
            "g_target": GraphPlot("T_BED", (0.2, 0.8, 0.8)),
            "t_actual": 0,
            "t_target": 0,
            "t_preheat": 65,
            "heating": False,
            "state": "cold",
            "btn-name": "heat-bed",
            "func-name": self.on_preheat_bed,
            "btn": None
        }
    }

    for tool in self.temps:
      # Add graphs
      self.graph.add_plot(self.temps[tool]["g_actual"])
      self.graph.add_plot(self.temps[tool]["g_target"])

      # Set up buttons
      btn = self.config.ui.get_object(self.temps[tool]["btn-name"])
      tap = Clutter.TapAction()
      btn.add_action(tap)
      tap.connect("tap", self.temps[tool]["func-name"])
      self.temps[tool]["btn"] = btn

    scale = GraphScale(self.graph_color, 0, 320, [0, 50, 100, 150, 200, 250, 300])
    self.graph.add_plot(scale)

    # set up temp label
    self.lbl_temp = self.config.ui.get_object("lbl-temp")
    self.ok_range = 4.0

  def update_temperatures(self, temp):
    time = temp['time']
    for tool in self.temps:
      if tool in temp:
        t = temp[tool]["actual"]
        plot = self.temps[tool]["g_actual"]
        plot.add_point(time, t)
        t = temp[tool]["target"]
        plot = self.temps[tool]["g_target"]
        plot.add_point(time, t)
    self.graph.refresh()

  def update_temperature_status(self, temp):
    for tool in self.temps:
      if tool in temp:
        self.temps[tool]["t_actual"] = temp[tool]["actual"]
        self.temps[tool]["t_target"] = temp[tool]["target"]
    if "tool1" in temp:
      self.lbl_temp.set_text("B:{} T0:{} T1:{}".format(
          temp["bed"]["actual"], temp["tool0"]["actual"], temp["tool1"]["actual"]))
    elif "bed" in temp:
      self.lbl_temp.set_text("B:{} T0:{}".format(temp["bed"]["actual"], temp["tool0"]["actual"]))

    # Update preheat button states
    self.update_states()

  # Retrieve the current state of the heating
  # elements
  def update_states(self):
    for tool in self.temps:
      if self.temps[tool]["t_target"] > 0:
        self.temps[tool]["heating"] = True
        diff = self.temps[tool]["t_target"] - self.temps[tool]["t_actual"]
        if abs(diff) < self.ok_range:
          self.temps[tool]["state"] = "heated"
          if tool == "bed":
            self.set_style_class(self.temps[tool]["btn"], "hot_bed")
          else:
            self.set_style_class(self.temps[tool]["btn"], "hot")
        elif diff > 0:
          self.temps[tool]["state"] = "heating"
          if tool == "bed":
            self.set_style_class(self.temps[tool]["btn"], "heating_bed")
          else:
            self.set_style_class(self.temps[tool]["btn"], "heating")
        else:
          self.temps[tool]["state"] = "cooling"
      else:
        if tool == "bed":
          self.set_style_class(self.temps[tool]["btn"], "cold_bed")
        else:
          self.set_style_class(self.temps[tool]["btn"], "cold")

  def on_preheat_tool0(self, button, action):
    if self.temps["tool0"]["heating"]:
      self.config.rest_client.set_tool_temp(0, 0)
      self.set_style_class(self.temps["tool0"]["btn"], "cold")
      self.temps["tool0"]["heating"] = False
    else:
      new_temp = self.temps["tool0"]["t_preheat"]
      self.config.rest_client.set_tool_temp(0, new_temp)
      self.set_style_class(self.temps["tool0"]["btn"], "heating")
      self.temps["tool0"]["heating"] = True

  def on_preheat_tool1(self, button, action):
    if self.temps["tool1"]["heating"]:
      self.config.rest_client.set_tool_temp(1, 0)
      self.set_style_class(self.temps["tool1"]["btn"], "cold")
      self.temps["tool1"]["heating"] = False
    else:
      new_temp = self.temps["tool1"]["t_preheat"]
      self.config.rest_client.set_tool_temp(1, new_temp)
      self.set_style_class(self.temps["tool1"]["btn"], "heating")
      self.temps["tool1"]["heating"] = True

  def on_preheat_tool2(self, button, action):
    if self.temps["tool2"]["heating"]:
      self.config.rest_client.set_tool_temp(2, 0)
      self.set_style_class(self.temps["tool2"]["btn"], "cold")
      self.temps["tool2"]["heating"] = False
    else:
      new_temp = self.temps["tool2"]["t_preheat"]
      self.config.rest_client.set_tool_temp(2, new_temp)
      self.set_style_class(self.temps["tool2"]["btn"], "heating")
      self.temps["tool2"]["heating"] = True

  def on_preheat_bed(self, button, action):
    if self.temps["bed"]["heating"]:
      self.config.rest_client.set_bed_temp(0)
      self.set_style_class(self.temps["bed"]["btn"], "cold_bed")
      self.temps["bed"]["heating"] = False
    else:
      new_temp = self.temps["bed"]["t_preheat"]
      self.config.rest_client.set_bed_temp(new_temp)
      self.set_style_class(self.temps["bed"]["btn"], "heating_bed")
      self.temps["bed"]["heating"] = True

  def set_style_class(self, btn, style_class):
    btn.set_from_file(self.config.style.style_to_filename(style_class))
