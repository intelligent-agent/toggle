import pytest
from os.path import join, abspath, dirname

clutter = pytest.importorskip("gi.repository.Clutter")

from toggle.StyleLoader import StyleLoader
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter


def test_style_loader(default_config):
  config = default_config
  config.file_base = abspath(join(dirname(__file__), ".."))
  styles = ["Plain", "Mixer", "Spitzy"]
  resolutions = ["1920x1080", "1280x720", "800x480"]

  Clutter.init(None)

  for style in styles:
    for res in resolutions:
      config['Screen']['width'] = res.split("x")[0]
      config['Screen']['height'] = res.split("x")[1]
      config['Screen']['rotation'] = "0"
      config['Style']['style'] = style
      loader = StyleLoader(config)
      assert (loader.load_ui(loader.ui_file_path))
