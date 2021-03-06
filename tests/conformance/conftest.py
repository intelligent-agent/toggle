import pytest
import mock
from os.path import join, abspath, dirname
from toggle.core.CascadingConfigParser import CascadingConfigParser


@pytest.fixture(scope="session")
def default_config():
  config_dir = join(dirname(__file__), "../../configs/")
  config = CascadingConfigParser([abspath(config_dir + "default.cfg")])
  config.splash = mock.Mock()
  config.push_updates = mock.Mock()
  return config


@pytest.fixture(scope="session")
def default_stage():
  import gi
  gi.require_version('Clutter', '1.0')
  from gi.repository import Clutter, GLib
  Clutter.init([])
  stage = Clutter.Stage()
  stage.set_size(800, 500)
  stage.set_title('Clutter - Cairo content')
  stage.set_user_resizable(True)
  return stage
