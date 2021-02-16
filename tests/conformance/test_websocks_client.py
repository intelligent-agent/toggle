import pytest
import requests
import requests_mock
import threading
import mock
import time

from toggle.core.WebSocksClient import WebSocksClient


def test_websocks_client_ok(default_config):

  client = WebSocksClient(default_config)

  def work():
    pass

  client.start()
  threading.Thread(target=work).start()
  while client.state < 2:
    pass
  assert client.state == 4
  client.stop()
  assert client.state == 0
