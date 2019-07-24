import pytest

pytest.importorskip("pyconnman")
from toggle.Network import ConnMan
from dbus.mainloop.glib import DBusGMainLoop


def test_connman(default_config):
  DBusGMainLoop(set_as_default=True)
  cm = ConnMan(default_config)
  assert (1)