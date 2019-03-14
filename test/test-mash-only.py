import subprocess
import logging
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Mx', '1.0')
gi.require_version('Mash', '0.3')
from gi.repository import Clutter, Mx, Mash, Cogl, GObject

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')

if __name__ == '__main__':
  Clutter.init(None)

  stage = Clutter.Stage()
  model = Mash.Model()
  data = Mash.Data()
  model.set_data(data)
  data.load(0, "/home/root/.octoprint/uploads/reel2.stl")
  v1 = Clutter.Vertex()
  v2 = Clutter.Vertex()
  data.get_extents(v1, v2)
  print(v1.z)
  print(v2.z)

  print(model.get_depth())

  color = Clutter.Color.from_string("#F00F")[1]
  model.set_color(color)
  model.set_progress(1)

  p = model.get_pipeline()
