# Networ connection manager
import socket 
import os
import gi



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
            return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        except socket.error, e:
            return "Network unreachable"

class ConnMan(Network):
    def __init__(self):
        Network.__init__(self)
        import pyconnman
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
            if "Name" in params:
                ap = {"name": params["Name"], "active": params["State"] == "online", "service": service}
            else:
                ap = {"name": "?", "active": False, "service": None}
            aps.append(ap)
        return aps

    def get_active_access_point(self):
        return None

    def ap_needs_password(self, ap):
        # Assume all APs need a password
        return True
    

    def connect(self, ap, passwd):
        print ap["service"]
        print "Connecting to "+ap["name"]+" with "+passwd
        return "OK"

class NetworkManager(Network):
    def __init__(self):
        Network.__init__(self)
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
            aps.append({"name": aap.get_ssid(), "active": True, "service": aap})
            aap_bssid = aap.get_bssid()
        for ap in self.wifi.get_access_points():
            i = {"name": ap.get_ssid(), "active": False, "service": ap}
            if ap.get_bssid() != aap_bssid:
                aps.append(i)
        return aps

    def get_active_access_point(self):
        return self.wifi.get_active_access_point()


    def connect(self, ap, passwd):
        print ap["service"]
        print "Connecting to "+ap["name"]+" with "+passwd
        return "OK"


if __name__ == "__main__":
    m = Network.get_manager()
    if m == "connman":
        n = ConnMan()
        print "Using Connman"
    elif m == "nm":
        n = NetworkManager()
        print "Using NetworkManager"
    else:
        print "Neither NetworkManager nor Connman was found"
        exit(1)

    print "Is wifi capable: "+str(n.has_wifi_capabilities())
    print "Is wifi Enabled: "+str(n.is_wifi_connected())
    print "Is ethernet capable: "+str(n.has_ethernet_capabilities())
    print "Is ethernet Enabled: "+str(n.is_ethernet_connected())
    for ap in n.get_access_points():
        print "*" if ap["active"] else " ",
        print ap["name"]
    print "IP: "+n.get_connected_ip()

    print n.connect(n.get_access_points()[0], "grim")
