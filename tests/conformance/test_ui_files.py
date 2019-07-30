import pytest
import json
from os.path import join, abspath, dirname

clutter = pytest.importorskip("gi.repository.Clutter")

from toggle.ui.StyleLoader import StyleLoader
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter


def test_style_loader(default_config):
  config = default_config
  config.file_base = abspath(join(dirname(__file__), "../.."))
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


def find(key, value):
  for k, v in (value.items()
               if isinstance(value, dict) else enumerate(value) if isinstance(value, list) else []):
    if k == key:
      yield v
    elif isinstance(v, (dict, list)):
      for result in find(key, v):
        yield result


def test_all_ui_files_have_correct_id_labels():
  ui_files = ["ui_1920x1080.json", "ui_1280x720.json", "ui_800x480.json"]
  file_base = abspath(join(dirname(__file__), "../../scripts/styles/templates"))
  ids = []
  for ui_file in ui_files:
    ui = file_base + "/" + ui_file
    f = open(ui)
    data = json.load(f)
    ids += list(find("id", data))
    f.close()
  all_ids = set(ids) - set(["text_xy", "text_z", "text_e"])

  for ui_file in ui_files:
    ui = file_base + "/" + ui_file
    f = open(ui)
    data = json.load(f)
    current_ids = list(find("id", data))
    for id in all_ids:
      if not id in current_ids:
        print(ui)
      assert (id in current_ids)
    f.close()
