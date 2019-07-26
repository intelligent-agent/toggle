import pytest

pytest.importorskip("NetworkManager")
from toggle.Network import NetworkManager
from dbus.mainloop.glib import DBusGMainLoop


def test_network_manager(default_config):
  DBusGMainLoop(set_as_default=True)
  cm = NetworkManager(default_config)
  assert (1)
