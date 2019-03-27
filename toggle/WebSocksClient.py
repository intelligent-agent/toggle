"""Simple Web socket client implementation using Tornado framework.
"""

from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket

import threading
import functools
import json
import time
import random
import string
import logging
import sys

from Event import PushUpdate

APPLICATION_JSON = 'application/json'

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60


class WebSocksClient():
  """
  Base for web socket clients.
  """

  CLOSED = 0
  CONNECTING = 1
  CONNECTED = 2
  FAILED = 3

  def __init__(self, config=None, host="ws://kamikaze.local"):
    self.config = config
    self.host = host
    self.connect_timeout = 60
    self.request_timeout = 60
    self._prefix = "/sockjs"
    self._r1 = str(random.randint(0, 1000))
    self._conn_id = self.random_str(8)
    self.url = host + '/'.join([self._prefix, self._r1, self._conn_id, 'websocket'])

    self.max_reconnects = 10
    self.state = WebSocksClient.CLOSED
    self.io_loop = ioloop.IOLoop.current()

  def connect(self):
    logging.debug("Connecting to " + self.url)
    self.state = WebSocksClient.CONNECTING
    self.conn = websocket.websocket_connect(
        self.url, io_loop=self.io_loop, callback=self._connect_callback)

  def send(self, data):
    """
    Send message to the server
      :param str data: message.
    """
    if not self._ws_connection:
      raise RuntimeError('Web socket connection is closed.')
    self._ws_connection.write_message(escape.utf8(json.dumps(data)))

  def close_conn(self):
    """
    Close connection.
    """
    if not self._ws_connection:
      raise RuntimeError('Web socket connection is already closed.')
    self._ws_connection.close()

  def _connect_callback(self, future):
    if future.exception() is None:
      self._ws_connection = future.result()
      self._on_connection_success()
      self._read_messages()
    else:
      self._on_connection_error(future.exception())

  @gen.coroutine
  def _read_messages(self):
    while True:
      msg = yield self._ws_connection.read_message()
      if msg is None:
        self._on_connection_close()
        break
      self._on_message(msg)

  def _on_message(self, msg):
    """
    This is called when new message is available from the server.
      :param str msg: server message.
    """
    #print(msg)
    data = msg[0]
    payload = msg[1:]
    if data == 'o':
      logging.debug("SockJS: Socket connected")
    elif data == 'c':
      logging.debug("SockJS: Socket disconnected, reason: " + str(payload))
    elif data == 'h':
      self.config.printer.flash_heartbeat()
      #logging.debug("SockJS: Heartbeat "+str(msg))
    elif data in ['a', 'm']:
      if self.config:
        self.parse_msg(payload)
      else:
        logging.debug(payload)
    else:
      logging.debug("Got garbled char " + str(msg) + " hex: " + str(int(msg, 16)))

  def _on_connection_success(self):
    """
    This is called on successful connection ot the server.
    """
    self.state = WebSocksClient.CONNECTED
    logging.debug('Websocket connected!')

  def _on_connection_close(self):
    """
    This is called when the server closes the connection.
    """
    self.state = WebSocksClient.CLOSED
    logging.debug('Websocket connection closed!')

  def _on_connection_error(self, exception):
    """
    This is called if the connection to the server could not be established.
    """
    self.state = WebSocksClient.FAILED
    self.io_loop.stop()
    logging.debug('Websocket connection error: %s', exception)

  def parse_msg(self, msg):
    try:
      data = json.loads(msg)[0]
      msg_type, payload = data.popitem()
      p = PushUpdate(msg_type, payload)
      self.config.push_updates.put(p)
    except Exception as e:
      logging.warning("Unable to parse message from Octoprint " + str(e))
      logging.warning("messsage was " + str(msg))

  def random_str(self, length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for c in range(length))

  def run(self):
    for i in range(self.config.getint("Rest", "timeout")):
      if self.running:
        self.config.splash.set_status("Connecting to {} ({})".format(self.host, i))
        logging.debug("Websocket connection attempt " + str(i))
        self.connect()
        self.io_loop.start()
        time.sleep(1)
    self.config.splash.set_status("Unable to connect to " + self.host)
    self.config.splash.enable_next()

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def stop(self):
    self.running = False
    self.io_loop.stop()
    self.thread.join()


def main():
  logging.basicConfig(
      level=logging.DEBUG,
      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
      datefmt='%m-%d %H:%M')

  #client = WebSocksClient(None, "ws://kamikaze.local")
  client = WebSocksClient(None, "ws://localhost")

  def work():
    for i in range(10):
      print i
      time.sleep(1)

  client.start()
  threading.Thread(target=work).start()
  time.sleep(10)
  client.stop()


if __name__ == '__main__':
  main()
