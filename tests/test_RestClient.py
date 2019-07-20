import pytest
import requests

from toggle.RestClient import RestClient


def test_get_list_of_files(default_config, requests_mock):
  requests_mock.get('http://localhost:5000/api/files?%7B%7D', json={})
  testRestclient = RestClient(default_config)
  assert (testRestclient.get_list_of_files() == {})


def test_select_tool(default_config, requests_mock):
  requests_mock.get('http://localhost:5000/api/files?%7B%7D', json={})
  testRestclient = RestClient(default_config)
  assert (testRestclient.get_list_of_files() == {})
