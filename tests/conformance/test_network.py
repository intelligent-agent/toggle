import pytest
from toggle.Network import ConnMan, NetworkManager
from dbus.mainloop.glib import DBusGMainLoop


def test_connman(default_config):
  DBusGMainLoop(set_as_default=True)
  cm = ConnMan(default_config)
  assert (1)


def test_network_manager(default_config):
  DBusGMainLoop(set_as_default=True)
  cm = NetworkManager(default_config)
  assert (1)
