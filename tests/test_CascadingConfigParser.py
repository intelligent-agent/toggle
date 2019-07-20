import unittest
import mock    # use mock.Mock etc
from os import listdir
from os.path import isfile, join


from toggle.CascadingConfigParser import CascadingConfigParser

class TestCascadingConfigParser(unittest.TestCase):
  def setUp(self):
    self.default = CascadingConfigParser(["../configs/default.cfg"])

  def test_all_config_files(self):
    path = "../configs/"
    config_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    for f in config_files:
        assert(self.default.check_file_valid(f))
