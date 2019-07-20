import pytest
from os.path import join, abspath, dirname
from toggle.CascadingConfigParser import CascadingConfigParser


@pytest.fixture(scope="session")
def default_config():
  config_dir = join(dirname(__file__), "../configs/")
  return CascadingConfigParser([abspath(config_dir + "default.cfg")])
