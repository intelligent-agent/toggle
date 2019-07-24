import pytest
import random
from toggle.Graph import Graph, GraphPlot, GraphScale
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, GLib


def test_graph_scale():
  scale = GraphScale((0, 0, 0, 128), -100, 100, [-50, 0, 50])
  assert (scale.line_y_pos(100, 0) == 50)
  assert (type(scale) == GraphScale)


def test_graph_plot():
  plot = GraphPlot("H", (0, 1, 0))
  assert (type(plot) == GraphPlot)


def test_graph():
  graph = Graph(800, 500)
  plot = GraphPlot("H", (0, 1, 0))
  plot.add_point(5, random.random() * 200 - 100)
  graph.refresh()
  assert (type(graph) == Graph)
