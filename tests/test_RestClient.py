import unittest
import mock    # use mock.Mock etc

from toggle.CascadingConfigParser import CascadingConfigParser
from toggle.RestClient import RestClient

class TestRestClient(unittest.TestCase):
  def setUp(self):
    config = CascadingConfigParser(["../configs/default.cfg"])
    self.testRestclient = RestClient(config)

  def test_get_list_of_files(self):
    self.testRestclient.get_list_of_files()