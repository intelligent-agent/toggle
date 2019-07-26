import pytest
import mock
import sys
sys.modules['gi'] = mock.MagicMock()
sys.modules['gi.repository'] = mock.MagicMock()
sys.modules['gi.repository.Clutter'] = mock.MagicMock()
sys.modules['cairo'] = mock.MagicMock()

from toggle.Graph import Graph, GraphPlot, GraphScale


def test_graph_plot(mocker):
  ctx = mock.Mock()
  plot = GraphPlot("H", (0, 1, 0))
  plot.add_point(0, 4)
  width = 10
  height = 20
  plot.draw(ctx, width, height)
  assert (ctx.line_to.call_count == 1)
  assert (plot.xy_values == ([0, width], [height - 4, height - 4]))
  plot.add_point(1, 6)
  plot.draw(ctx, 100, 100)
  assert (ctx.line_to.call_count == 2)
  assert (plot.xy_values == ([0, 100], [96.0, 94.0]))


def test_graph_scale():
  scale = GraphScale((0, 0, 0, 128), -100, 100, [-50, 0, 50])
  assert (scale.line_y_pos(100, 0) == 50)
  assert (type(scale) == GraphScale)


def test_graph():
  #with mock.patch('gi.repository.Clutter.Actor', autospec=True) as MockActor:
  ctx = mock.Mock()
  canvas = mock.Mock()
  graph = Graph(800, 500)
  graph.draw2(canvas, ctx, 10, 10)
  print(graph)
  #assert (0)
