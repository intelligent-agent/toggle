from threading import Thread
import time
import httplib
import random
import string
import socket
import json

from Event import Event
import logging


""" SockJS Client class  """
class SocksClient(Thread):
    TRANSPORT = "xhr_streaming"

    _wait_thread = 0
    _prefix = ""
    _host = ""
    _port = 80

    def __init__(self, config, prefix="/sockjs", host = "localhost", port = 5000):
        self.config = config
        self._prefix = prefix
        self._host = host
        self._port = port
        self.running = False
        Thread.__init__(self)

    def connect(self):
        self.get_socket_info()
        self.running = True
        self.start()

    def disconnect(self):
        self.running = False

    def run(self):
        conn = httplib.HTTPConnection(self._host, self._port)
        self._r1 = str(random.randint(0, 1000))
        self._conn_id = self.random_str(8)
        url = '/'.join([self._prefix, self._r1, self._conn_id, 'xhr_streaming'])
        try:
            conn.request('POST', url)
            response = conn.getresponse()
            sock = socket.fromfd(response.fileno(), socket.AF_INET, socket.SOCK_STREAM)
            data = 1
            msgs = self.linesplit(sock)
        except Exception as e:
            logging.warning("Unable to post request "+str(e))
            return
        while self.running: 
            msg =  msgs.next()
            if len(msg) == 0:
                continue
            data = msg[0]
            payload = msg[1:]
            if data == 'o':
                logging.info("Socket connected")
            elif data == 'c':
                if "[" in payload and "]" in payload:
                    logging.info("Socket disconnected, reason: "+str(payload))
                    return
                else:
                    logging.warning("Corrupt close frame: "+str(msg))
            elif data == 'h':
                #logging.info("Heartbeat "+str(msg))
                pass
            elif data == 'a':
                if "[" in payload and "]" in payload:
                    self.parse_msg(payload)
                else:
                    logging.warning("Corrupt message "+str(msg))
            elif data == 'm':
                print "m: "+payload
            else:
                #print "Got garbled char "+str(msg)+" hex: "+str(int(msg, 16))
                pass
        time.sleep(0)
        logging.info("server disconnected")

    def linesplit(self, socket):
        # H/T to Aaron Watters for this!
        # stackoverflow.com/questions/822001/python-sockets-buffering
        #socket.settimeout(1.0)
        buffer = socket.recv(4096)
        buffering = True
        while buffering:
            if "\r\n" in buffer:
                (line, buffer) = buffer.split("\r\n", 1)
                yield line 
            else:
                more = socket.recv(4096)
                if not more:
                    buffering = False
                else:
                    buffer += more
        if buffer:
            yield buffer

    def get_socket_info(self):
        conn = 0
        try:
            conn = httplib.HTTPConnection(self._host, self._port)
            conn.request('GET', '/sockjs/info')
            response = conn.getresponse()
            logging.info(str(response.status)+" "+response.reason+" "+response.read())
        except Exception as e:
            logging.warning("Unable to get socket info "+str(e))
        finally:
            if not conn: 
                conn.close()

    def send(self, message):
        conn = httplib.HTTPConnection(self._host, self._port)
        url = '/'.join([self._prefix, self._r1, self._conn_id, 'xhr_send'])
        conn.request('POST', url, "[" + message + "]", {'Content-Type': 'text/plain'})
        print "Sent: ", conn.getresponse().status, conn.getresponse().reason
        return conn.getresponse().status in (200, 204)

    def parse_msg(self, msg):
        try:
            data = json.loads(msg)
            for etype in data:
                if "connected" in etype: 
                    #print "Got connected"
                    self.config.connected = etype["connected"]
                    #logging.info("Data is "+str(self.config.connected))
                elif "current" in etype: 
                    self.config.state = etype["current"]
                    self.config.printer.update_printer_state(etype["current"]["state"])
                    self.config.printer.update_temperatures(etype["current"]["temps"])
                elif "history" in etype:
                    #print "Got history"
                    self.config.history = etype["history"]
                    #logging.info("History is "+str(self.config.history))
                elif "event" in etype:
                    #print "got event"
                    evt_type = etype["event"]["type"]
                    payload = etype["event"]["payload"]
                    e = Event(evt_type, payload)
                    self.config.events.put(e)
                elif "slicingProgress" in etype:
                    #print "got slicing progress "+str(etype["slicingProgress"])
                    pass
                elif "state" in etype: 
                    print "got state"
                elif "timelapse" in etype: 
                    #print "got timelapse"
                    pass
                else:
                    print "Unknown event type "+str(etype)
        except:
            logging.warning("Unable to parse message from Octoprint ")
            logging.warning("messsage was "+str(msg))
            raise

    def random_str(self, length):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for c in range(length))


if __name__ == "__main__":
    import time

    client = SocksClient()
    client.connect()

    time.sleep(5)

    if client.send("{ \"value\": 123}"):
        print "Message sent"

    if client.send("\"echome\""):
        print "Echo message sent"

    client.disconnect()


