import pytest
import requests
import requests_mock
import json

from toggle.core.RestClient import RestClient


@requests_mock.Mocker(kw='mock')
def test_connection_ok(default_config, **kwargs):
  kwargs['mock'].get('http://localhost:5000/api/version')
  assert RestClient(default_config).connection_ok() == True


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


def _config_with(password, apikey):
  """A config as toggle-runfirst leaves it, rather than as the image ships it."""
  import mock
  from os.path import join, abspath, dirname
  from toggle.core.CascadingConfigParser import CascadingConfigParser
  cfg = CascadingConfigParser(
    [abspath(join(dirname(__file__), "../../configs/default.cfg"))])
  cfg.splash = mock.Mock()
  cfg.push_updates = mock.Mock()
  cfg.set("OctoPrint", "password", password)
  cfg.set("OctoPrint", "authentication", apikey)
  return cfg


def test_credentials_not_ready_on_a_fresh_image(default_config):
  # default.cfg ships REPLACE_ME, which is what a board sitting at OctoPrint's
  # setup wizard looks like. No login should be attempted from that state.
  assert RestClient(default_config).credentials_ready() is False


def test_credentials_not_ready_with_an_empty_api_key():
  # What local.cfg actually contains before toggle-runfirst runs: a user, and
  # an authentication line with nothing after it.
  assert RestClient(_config_with("REPLACE_ME", "")).credentials_ready() is False


def test_credentials_ready_once_provisioned():
  assert RestClient(_config_with("s3cret", "an-api-key")).credentials_ready() is True


# login() fetches / first, to pick up the double-submit CSRF cookie that
# OctoPrint requires on /api/login. Both of these tests have to mock that GET:
# without it the request fails against a localhost nobody is serving, login()
# returns INVALID-SESSION from the ConnectionError, and neither test reaches the
# POST it is about. That made test_login_ok fail outright and, worse, made
# test_login_status_code_403 pass without ever exercising a 403.
def test_login_ok(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.get('http://localhost:5000/')
    m.post('http://localhost:5000/api/login', json={"session": "pizza"})
    client = RestClient(default_config)
    assert client.login() == "pizza"


def test_login_status_code_403(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.get('http://localhost:5000/')
    m.post('http://localhost:5000/api/login', status_code=403)
    client = RestClient(default_config)
    assert client.login() == "INVALID-SESSION"


def test_start_job(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/job', status_code=204)
    client = RestClient(default_config)
    assert client.start_job()


def test_pause_job(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/job', status_code=204)
    client = RestClient(default_config)
    assert client.pause_job()


def test_cancel_job(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/job', status_code=204)
    client = RestClient(default_config)
    assert client.cancel_job()


def test_resume_job(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/job', status_code=204)
    client = RestClient(default_config)
    assert client.resume_job()


def test_send_gcode(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/command', status_code=204)
    client = RestClient(default_config)
    assert client.send_gcode("G0 X0")


def test_set_bed_temp(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/bed', status_code=204)
    client = RestClient(default_config)
    assert client.set_bed_temp(42)


def test_set_tool_temp(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/tool', status_code=204)
    client = RestClient(default_config)
    assert client.set_tool_temp(0, 42)


def test_select_file(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/files/local/Dolf-Lundgren', status_code=204)
    client = RestClient(default_config)
    assert client.select_file("Dolf-Lundgren")


def test_jog(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/printhead', status_code=204)
    client = RestClient(default_config)
    assert client.jog({"X": 42})
    client.jog({"X": 42})


def test_home(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/printhead', status_code=204)
    client = RestClient(default_config)
    assert client.home("X")


def test_extrude(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/tool', status_code=204)
    client = RestClient(default_config)
    assert client.extrude(7)


def test_select_tool(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/printer/tool', status_code=204)
    client = RestClient(default_config)
    assert client.select_tool(0)


def test_download_model(default_config):
  with requests_mock.Mocker() as m:
    m.get("http://chuck-norris.com", content=b"Bruce-Willis")
    client = RestClient(default_config)
    assert client.download_model("http://chuck-norris.com") == b"Bruce-Willis"


def test_get_slicers(default_config):
  with requests_mock.Mocker(real_http=True) as m:
    m.post('http://localhost:5000/api/slicing', json={"arnhold-slicer": {}})
    client = RestClient(default_config)
    assert client.get_slicers()["arnhold-slicer"] == {}
