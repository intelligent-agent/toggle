# Model
import os.path
import logging
from gi.repository import Clutter, Mx, Cogl, Mash


class Model(Mash.Model):
  def __init__(self, config):
    super(Model, self).__init__()

    self.config = config
    self.model = config.ui.get_object("model")
    color_str = config.get("System", "model-color")
    self.color = Clutter.Color.from_string(color_str)[1]
    self.loader = config.ui.get_object("loader")
    self.loader.set_from_file(config.get("System", "loader"))

    self.model_data = Mash.Data()
    self.model.set_data(self.model_data)
    self.v_min = Clutter.Vertex()
    self.v_max = Clutter.Vertex()
    self.depth = 0

    self.t = Clutter.PropertyTransition(property_name='rotation-angle-z')
    self.t.set_from(0)
    self.t.set_to(360)
    self.t.set_duration(3000)
    self.t.set_animatable(self.loader)
    self.t.set_repeat_count(-1)
    self.t.start()

    # Set up the light
    self.light_set = Mash.LightSet()
    vp = config.ui.get_object("volume-viewport")

    # Directional
    self.light_directional = Mash.DirectionalLight()
    self.light_set.add_light(self.light_directional)

    # Point light
    self.light_point = Mash.PointLight()
    self.light_set.add_light(self.light_point)

    # Add the model the lights to the volume viewport
    vp.add_child(self.light_directional)
    vp.add_child(self.light_point)

    cm = Cogl.Matrix()
    m = Clutter.matrix_init_from_array(cm, [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    config.ui.get_object("model-flipper").set_transform(m)

    self.model.connect("show", self.model_loaded)

    self.model.set_light_set(self.light_set)
    self.model.set_color(self.color)

  # Load model is a fairly CPU intensive
  # operation on complex models. On BBB it can take several seconds to load
  # Treefrog or Benchy etc. It would therefore be better to have the
  # data loading happen in a separate thread, so that the loading icon can be
  # shown uninterrupted. UI operations must then be separated out, since they
  # are required to run in the min thread.
  def load_model(self, filename):
    self.model.hide()
    self.filename = filename
    path = self.config.get("System", "model_folder") + "/" + filename
    if not os.path.isfile(path):
      logging.warning(path + " is not a file")
    try:
      self.model_data.load(0, path)
      #self.model.load_from_file(0, path)
      self.model.set_data(self.model_data)
    except BaseException:
      logging.warning("Unable to open model " + path)
      raise
      return
    self.model_data.get_extents(self.v_min, self.v_max)
    (self.width, self.height) = self.model.get_size()
    self.depth = self.v_max.z - self.v_min.z
    self.model.set_y(-0.01 - self.depth / 2.0)    # Prevent Z-fighting
    self.model.set_x(-self.width / 2.0)
    self.model.set_z_position(-self.height / 2.0)
    self.set_progress(0)
    self.model.show()

  # Hide the spinner/loader when done.
  def model_loaded(self, model):
    self.loader.hide()

  def select_none(self):
    self.loader.hide()
    self.model.hide()

  def set_progress(self, progress):
    # TODO: progress now assumes that the model starts
    # at a distance of 0 above origin in z-direction.
    # This should be removed from the depth.
    height_above_platform = self.v_min.z
    self.model.set_progress(self.depth * progress + height_above_platform)

  def set_slicing_progress(self, progress):
    # TODO: Change color showing the progress of the
    # slicing.
    pass
