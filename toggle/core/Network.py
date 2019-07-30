# Network connection manager
import socket
import os
import uuid
import logging


class Network:
  def __init__(self):
    self.ap_removed_cb = None
    self.ap_added_cb = None
    self.ap_prop_changed_cb = None
    self.ap_state_changed_cb = None

  @staticmethod
  def get_manager(config):
    cmd = os.popen("systemctl | grep connman").read()
    if "active" in cmd:
      logging.debug("Using Connman")
      return ConnMan(config)
    cmd = os.popen("systemctl | grep NetworkManager").read()
    if "active" in cmd:
      logging.debug("Using NetworkManager")
      from .SecretAgent import SecretAgent
      config.agent = SecretAgent(config)
      return NetworkManager(config)
    logging.warning("Neither NetworkManager nor Connman was found")
    return None

  def get_connected_ip(self):
    try:
      return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
              for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    except socket.error as e:
      return "Network unreachable"


class ConnMan(Network):
  def __init__(self, config):
    Network.__init__(self)
    self.config = config
    import pyconnman
    import dbus
    self.dbus = dbus
    self.p = pyconnman
    try:
      self.manager = pyconnman.ConnManager()
    except self.dbus.exceptions.DBusException as e:
      logging.warning("Connman not a known service on DBus")
      return
    self.technologies = self.manager.get_technologies()
    self.wifi = None
    self.ethernet = None
    self.bluetooth = None
    self.aps_by_path = {}

    for t in self.technologies:
      (path, params) = t
      if params['Name'] == "WiFi":
        self.wifi = pyconnman.ConnTechnology(path)
        self._start_agent()
      elif params['Name'] == "Wired":
        self.ethernet = pyconnman.ConnTechnology(path)
      elif params['Name'] == "Bluetooth":
        self.bluetooth = t
    self.manager.add_signal_receiver(self.services_changed, self.manager.SIGNAL_SERVICES_CHANGED,
                                     None)
    if self.wifi:
      self.wifi.add_signal_receiver(self.wifi_changed, self.wifi.SIGNAL_PROPERTY_CHANGED, None)

  def wifi_changed(self, signal_name, user_arg, prop, value):
    print("wifi changed")

  def property_changed(self, signal_name, ap, prop, value):
    if self.ap_prop_changed_cb:
      if prop in ["Strength", "State"]:
        self.ap_prop_changed_cb(ap)

  def services_changed(self, signal_name, user_arg, services, signatures):
    self.config.settings.add_all_aps()

  def has_wifi_capabilities(self):
    return not not self.wifi

  def has_ethernet_capabilities(self):
    return not not self.ethernet

  def is_wifi_connected(self):
    if not self.has_wifi_capabilities():
      return False
    return

  def is_ethernet_connected(self):
    if not self.has_ethernet_capabilities():
      return False
    return False

  def get_access_points(self):
    aps = []
    try:
      for service in self.manager.get_services():
        (path, params) = service
        if params["Type"] == "wifi":
          if path in self.aps_by_path:
            ap = self.aps_by_path[path]
          else:
            ap = {
                "name": params["Name"] if "Name" in params else "?",
                "active": (params["State"] == "online") if "State" in params else False,
                "service": self.p.ConnService(path),
                "strength": params["Strength"] if "Strength" in params else "0",
                "security": params["Security"] if "Security" in params else "?",
                "object_path": path
            }
            ap["service"].add_signal_receiver(self.property_changed,
                                              self.wifi.SIGNAL_PROPERTY_CHANGED, ap)
            self.aps_by_path[path] = ap
          aps.append(ap)
    except self.dbus.exceptions.DBusException:
      pass
    return aps

  def get_active_access_point(self):
    return None

  def ap_needs_password(self, ap):
    service = self.p.service.ConnService(ap["path"])

    if "none" in ap["security"]:
      return False
    return True

  # Perform a wifi scan
  def scan(self):
    self.wifi.scan()

  def add_connection_finished_cb(self, cb):
    self.connection_finished_cb = cb

  def connection_finished_cb(self, other):
    print(other)

  # Update the password on an existing AP.
  def update_password(self, ap, passwd):
    pass

  # Add a connection not previously seen
  def add_connection(self, ap):
    pass

  def _start_agent(self):
    params = {
        'name': None,
        'ssid': None,
        'identity': None,
        'username': None,
        'password': None,
        'passphrase': None,
        'wpspin': None,
    }
    try:
      agent_path = '/no/iagent/connman'
      self.agent = self.p.SimpleWifiAgent(agent_path)
      self.agent.set_service_params('*', params['name'], params['ssid'], params['identity'],
                                    params['username'], params['password'], params['passphrase'],
                                    params['wpspin'])
      self.manager.register_agent(agent_path)
    except self.dbus.exceptions.DBusException:
      print('Unable to complete:', sys.exc_info())

  def activate_connection(self, ap):
    try:
      ap["service"].connect()
    except self.dbus.exceptions.DBusException as e:
      logging.warning(e)


class NetworkManager(Network):
  def __init__(self, config):
    Network.__init__(self)
    import NetworkManager as SystemNetworkManager
    self.nm = SystemNetworkManager
    self.devices = self.nm.NetworkManager.GetDevices()
    self.wifi = None
    self.ethernet = None
    for dev in self.devices:
      if dev.DeviceType == SystemNetworkManager.NM_DEVICE_TYPE_WIFI:
        self.wifi = dev
        self.wifi.OnAccessPointAdded(self.ap_added)
        self.wifi.OnAccessPointRemoved(self.ap_removed)
        self.wifi.OnStateChanged(self.ap_state_changed)
      if dev.DeviceType == SystemNetworkManager.NM_DEVICE_TYPE_ETHERNET:
        self.ethernet = dev
    self.aps_by_path = {}

  def has_wifi_capabilities(self):
    return not not self.wifi

  def has_ethernet_capabilities(self):
    return not not self.ethernet

  def is_wifi_connected(self):
    if not self.has_wifi_capabilities():
      return False
    return self.wifi.State == self.nm.NM_DEVICE_STATE_ACTIVATED

  def is_ethernet_connected(self):
    if not self.has_ethernet_capabilities():
      return False
    return self.ethernet.State == self.nm.NM_DEVICE_STATE_ACTIVATED

  def wrap_ap(self, ap):
    aap = self._active_access_point()
    return {
        "name": ap.Ssid,
        "active": ap.HwAddress == aap.HwAddress if aap else False,
        "service": ap,
        "strength": ap.Strength,
        "password": None,
        "object_path": ap.object_path
    }

  def get_access_points(self):
    aps = []
    for ap in self.wifi.SpecificDevice().GetAccessPoints():
      try:
        wap = self.wrap_ap(ap)
        self.save_ap(wap, ap.object_path)
        aps.append(wap)
        ap.OnPropertiesChanged(self.ap_prop_changed)
      except self.nm.ObjectVanished:
        pass
      except AttributeError:
        pass
    return aps

  def get_active_access_point(self):
    try:
      ap = self._active_access_point()
      if ap:
        return self.wrap_ap(ap)
    except self.nm.ObjectVanished:
      pass

  def _active_access_point(self):
    ap = self.wifi.SpecificDevice().ActiveAccessPoint
    if ap and hasattr(ap, "HwAddress"):
      return ap

  # Perform a wifi scan
  def scan(self):
    self.wifi.request_scan()

  def get_ap_by_path(self, path):
    if path in self.aps_by_path:
      return self.aps_by_path[path]
    return None

  def save_ap(self, ap, path):
    self.aps_by_path[path] = ap

  def ap_added(self, dev, interface, signal, access_point):
    try:
      if hasattr(access_point, "HwAddress"):
        access_point.OnPropertiesChanged(self.ap_prop_changed)
        ap = self.wrap_ap(access_point)
        self.save_ap(ap, ap["object_path"])
        if self.ap_added_cb:
          self.ap_added_cb(ap)
    except self.nm.ObjectVanished:
      pass

  def ap_removed(self, dev, interface, signal, access_point):
    try:
      ap = self.get_ap_by_path(access_point.object_path)
      if self.ap_removed_cb and ap:
        self.ap_removed_cb(ap)
    except self.nm.ObjectVanished:
      pass

  def ap_state_changed(self, nm, interface, signal, old_state, new_state, reason):
    try:
      if self.ap_state_changed_cb:
        self.ap_state_changed_cb(nm, self.nm.const('device_state', new_state))
    except self.nm.ObjectVanished:
      pass

  def ap_prop_changed(self, ap, interface, signal, properties):
    try:
      if self.ap_prop_changed_cb and hasattr(ap, "HwAddress"):
        self.ap_prop_changed_cb(self.wrap_ap(ap))
    except self.nm.ObjectVanished:
      pass

  def add_connection(self, ap):
    # Assume wpa-psk security
    conn = None
    try:
      if ap["service"].RsnFlags & self.nm.NM_802_11_AP_SEC_KEY_MGMT_PSK:
        new_connection = {
            '802-11-wireless': {
                'mode': 'infrastructure',
                'security': '802-11-wireless-security',
                'ssid': ap["name"]
            },
            '802-11-wireless-security': {
                'auth-alg': 'open',
                'key-mgmt': 'wpa-psk'
            },
            'connection': {
                'id': ap["name"],
                'type': '802-11-wireless',
                'uuid': str(uuid.uuid4())
            },
            'ipv4': {
                'method': 'auto'
            },
            'ipv6': {
                'method': 'auto'
            }
        }
        conn = self.nm.Settings.AddConnection(new_connection)
      else:
        logging.warning("Only WPA-PSK security implemented")
    except self.nm.ObjectVanished:
      pass
    return conn

  def get_known_connections(self):
    connections = self.nm.Settings.ListConnections()
    return dict([(x.GetSettings()['connection']['id'], x) for x in connections])

  # Activate a Wifi AP/SSID
  def activate_connection(self, ap):
    if self.is_known_connection(ap):
      connections = self.get_known_connections()
      conn = connections[ap["name"]]
    else:
      conn = self.add_connection(ap)
    try:
      self.nm.NetworkManager.ActivateConnection(conn, self.wifi, "/")
    except self.nm.ObjectVanished:
      pass

  def is_known_connection(self, ap):
    return ap["name"] in self.get_known_connections()


if __name__ == "__main__":
  m = Network.get_manager()
  if m == "connman":
    n = ConnMan()
    print("Using Connman")
  elif m == "nm":
    n = NetworkManager()
    print("Using NetworkManager")
  else:
    print("Neither NetworkManager nor Connman was found")
    exit(1)

  print("Is wifi capable: " + str(n.has_wifi_capabilities()))
  print("Is wifi Enabled: " + str(n.is_wifi_connected()))
  print("Is ethernet capable: " + str(n.has_ethernet_capabilities()))
  print("Is ethernet Enabled: " + str(n.is_ethernet_connected()))
  for ap in n.get_access_points():
    print(("*" if ap["active"] else " ") + ap["name"])
    print(ap["service"].WpaFlags)
  print("IP: " + n.get_connected_ip())

  print(n.activate_connection(n.get_access_points()[0]))
