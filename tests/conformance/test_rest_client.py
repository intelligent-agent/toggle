import pytest
import requests
import requests_mock
import json

from toggle.RestClient import RestClient


def test_get_list_of_files(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.get('http://localhost:5000/api/files', json={})
    testRestclient = RestClient(default_config)
    assert (testRestclient.get_list_of_files() == {})


def test_select_tool(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/tool')
    testRestclient = RestClient(default_config)
    assert (testRestclient.select_tool(0))
