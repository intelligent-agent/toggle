import gi
gi.require_version('Mx', '2.0')
gi.require_version('Clutter', '1.0')
gi.require_version('Mash', '0.3')
from gi.repository import Clutter, Mx, Mash
import logging
import os


class StyleLoader:
  def __init__(self, config):
    self.config = config
    config.screen_width = config.getint("Screen", "width")
    config.screen_height = config.getint("Screen", "height")
    config.screen_rot = config.getint("Screen", "rotation")
    config.screen_full = config.getboolean("Screen", "fullscreen")
    self.style_type = self.config.get("Style", "style")
    style_path = os.path.join(config.file_base, "styles", self.style_type)
    self.img_path = style_path
    if config.screen_rot in [90, 270]:
      width = config.screen_height
      height = config.screen_width
    else:
      width = config.screen_width
      height = config.screen_height
    ui_file = "ui_{}x{}.json".format(width, height)
    self.ui_file_path = os.path.join(style_path, ui_file)
    style_file = "style.css"
    self.style_file_path = os.path.join(style_path, style_file)
    logo_file_name = self.logo_for_screen_width(config.screen_width)
    self.logo_file_path = os.path.join(style_path, logo_file_name)

  def load_from_config(self):
    self.load_style(self.style_file_path)
    self.load_ui(self.ui_file_path)

  def load_style(self, filename):
    self.style = Mx.Style.get_default()
    self.style.load_from_file(filename)

  def load_ui(self, filename):
    self.ui = Clutter.Script()
    try:
      self.ui.load_from_file(filename)
    except BaseException as e:
      logging.warning(e)
      return False
    return True

  def do_screen_rotation(self):
    # Flip and move the stage to the right location
    # This has to be done in the application, since it is a
    # fbdev app
    if self.config.screen_rot == 90:
      self.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
      self.ui.get_object("all").set_position(self.config.screen_width, 0)
    elif self.config.screen_rot == 270:
      self.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
      self.ui.get_object("all").set_position(0, self.config.screen_height)
    elif self.config.screen_rot == 180:
      self.ui.get_object("all").set_pivot_point(0.5, 0.5)
      self.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 180.0)
    if self.config.screen_full:
      self.config.stage.set_fullscreen(True)

  def logo_for_screen_width(self, width):
    return {
        480: "logo_400.png",
        800: "logo_400.png",
        720: "logo_600.png",
        1280: "logo_600.png",
        1080: "logo_900.png",
        1920: "logo_900.png"
    }[width]

  def style_to_filename(self, style_class):
    return "{}/{}".format(
        self.img_path, {
            "arrow": "arrow_128.png",
            "arrow_disabled": "arrow_disabled_128.png",
            "cold": "heater_cold_128.png",
            "heating": "heater_heating_128.png",
            "hot": "heater_hot_128.png",
            "heating_bed": "heater_bed_heating_128.png",
            "cold_bed": "heater_bed_cold_128.png",
            "hot_bed": "heater_bed_hot_128.png"
        }[style_class])

  def get_missing_model_filename(self):
    return os.path.join(self.config.file_base, "models/missing-model.stl")

  def get_plate_filename(self):
    plate_name = self.style_type = self.config.get("Style", "plate")
    return os.path.join(self.config.file_base, "platforms/", plate_name)
