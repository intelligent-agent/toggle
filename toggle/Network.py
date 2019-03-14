# Network connection manager
import socket
import os


class Network:
  def __init__(self):
    pass

  @staticmethod
  def get_manager():
    cmd = os.popen("systemctl | grep connman").read()
    if "active" in cmd:
      return "connman"
    cmd = os.popen("systemctl | grep NetworkManager").read()
    if "active" in cmd:
      return "nm"
    return None

  def get_connected_ip(self):
    try:
      return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
              for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    except socket.error as e:
      return "Network unreachable"


class ConnMan(Network):
  def __init__(self):
    Network.__init__(self)
    import pyconnman
    import dbus
    self.dbus = dbus
    self.p = pyconnman
    self.manager = pyconnman.ConnManager()
    self.technologies = self.manager.get_technologies()
    self.wifi = None
    self.ethernet = None
    self.bluetooth = None

    for t in self.technologies:
      (path, params) = t
      if params['Name'] == "WiFi":
        self.wifi = t
      elif params['Name'] == "Wired":
        self.ethernet = t
      elif params['Name'] == "Bluetooth":
        self.bluetooth = t

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
    for service in self.manager.get_services():
      (path, params) = service
      ap = {
          "name": ["Name"] if "Name" in params else "?",
          "active": (params["State"] == "online") if "State" in params else False,
          "service": service,
          "strength": params["Strength"] if "Strength" in params else "?",
          "security": params["Security"] if "Security" in params else "?",
          "path": path
      }
      aps.append(ap)
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
      agent_path = "/test/agent"
      agent = self.p.SimpleWifiAgent(agent_path)
      agent.set_service_params('*', params['name'], params['ssid'], params['identity'],
                               params['username'], params['password'], params['passphrase'],
                               params['wpspin'])
      services[agent_path] = agent
      manager.register_agent(agent_path)
    except dbus.exceptions.DBusException:
      print('Unable to complete:', sys.exc_info())

  def activate_connection(self, ap):
    service = self.p.service.ConnService(ap["path"])
    try:
      service.connect()
    except self.dbus.exceptions.DBusException as e:
      return "ERROR"
    return "OK"


class NetworkManager(Network):
  def __init__(self):
    Network.__init__(self)
    import NetworkManager as SystemNetworkManager
    self.nm = SystemNetworkManager
    self.devices = self.nm.NetworkManager.GetDevices()
    self.wifi = None
    self.ethernet = None
    for dev in self.devices:
      if dev.DeviceType == SystemNetworkManager.NM_DEVICE_TYPE_WIFI:
        self.wifi = dev
      if dev.DeviceType == SystemNetworkManager.NM_DEVICE_TYPE_ETHERNET:
        self.ethernet = dev

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

  def get_access_points(self):
    aps = []
    aap = self.wifi.ActiveAccessPoint if self.wifi.State == self.nm.NM_DEVICE_STATE_ACTIVATED else None

    for ap in self.wifi.SpecificDevice().GetAccessPoints():
      if hasattr(self.wifi.SpecificDevice().ActiveAccessPoint, "HwAddress"):
        i = {
            "name": ap.Ssid,
            "active": ap.HwAddress == self.wifi.SpecificDevice().ActiveAccessPoint.HwAddress,
            "service": ap,
            "strength": ap.Strength
        }
        aps.append(i)
    return aps

  def get_active_access_point(self):
    return self.wifi.get_active_access_point()

  def ap_needs_password(self, ap):
    # Assume all APs need a password
    return False

  # Perform a wifi scan
  def scan(self):
    self.wifi.request_scan()

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

  # Activate a Wifi AP/SSID
  def activate_connection(self, ap):
    connections = self.nm.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
    conn = connections[ap["name"]]
    self.nm.NetworkManager.ActivateConnection(conn, self.wifi, "/")
    return "OK"


class NetworkManagerGI(Network):
  def __init__(self):
    Network.__init__(self)
    import gi
    gi.require_version('NetworkManager', '1.0')
    gi.require_version('NMClient', '1.0')
    from gi.repository import NetworkManager, NMClient
    self.nm = NetworkManager
    self.nmc = NMClient
    self.client = self.nmc.Client.new()
    self.devices = self.client.get_devices()
    self.access_points = []
    self.wifi = None
    self.ethernet = None

    for dev in self.devices:
      if dev.get_device_type() == self.nm.DeviceType.WIFI:
        self.wifi = dev
      if dev.get_device_type() == self.nm.DeviceType.ETHERNET:
        self.ethernet = dev

  def has_wifi_capabilities(self):
    return not not self.wifi

  def has_ethernet_capabilities(self):
    return not not self.ethernet

  def is_wifi_connected(self):
    if not self.has_wifi_capabilities():
      return False
    return self.wifi.get_state() == self.nm.DeviceState.ACTIVATED

  def is_ethernet_connected(self):
    if not self.has_ethernet_capabilities():
      return False
    return self.ethernet.get_state() == self.nm.DeviceState.ACTIVATED

  def get_access_points(self):
    aps = []
    aap = self.wifi.get_active_access_point()
    aap_bssid = ""
    if aap is not None:
      aps.append({
          "name": aap.get_ssid(),
          "active": True,
          "service": aap,
          "strength": aap.get_strength()
      })
      aap_bssid = aap.get_bssid()
    for ap in self.wifi.get_access_points():
      i = {"name": ap.get_ssid(), "active": False, "service": ap, "strength": ap.get_strength()}

      if ap.get_bssid() != aap_bssid:
        aps.append(i)
    return aps

  def get_active_access_point(self):
    return self.wifi.get_active_access_point()

  # Perform a wifi scan
  def scan(self):
    self.wifi.request_scan()

  def add_connection_finsihed_cb(self, cb):
    self.connection_finished_cb = cb

  def connection_finished_cb(self, other):
    print(other)

  # Connect to a WIFI AP
  def activate_connection(self, ap, passwd):
    #self.con = self.nm.Connection()
    #self.s_con = self.nm.SettingConnection()

    specific_object = ""
    #s_wifi = conn.get_setting_wireless()
    self.client.add_and_activate_connection(None, self.wifi, ap["service"],
                                            self.connection_finished_cb)
    print(ap["service"])
    print("Connecting to " + ap["name"] + " with " + passwd)
    return "OK"


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
    #print (ap["strength"],)
    print("*" if ap["active"] else " ", )
    print(ap["name"])
  print("IP: " + n.get_connected_ip())

  print ("Needs password: " + \
      str(n.ap_needs_password(n.get_access_points()[0])))
  print(n.activate_connection(n.get_access_points()[0]))
