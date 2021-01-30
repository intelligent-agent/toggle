import pytest
import requests
import requests_mock
import json

from toggle.core.RestClient import RestClient


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


def test_login_ok(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/login', json={"session": "pizza"})
    client = RestClient(default_config)
    assert client.login() == "pizza"


def test_login_status_code_403(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/login', status_code=403)
    client = RestClient(default_config)
    assert client.login() == "INVALID-SESSION"
