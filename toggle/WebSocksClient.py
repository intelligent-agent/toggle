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
import asyncio

from .Event import PushUpdate

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

  def __init__(self, config=None):
    self.config = config
    host = config.get("Server", "host")
    port = str(config.get("Server", "port"))
    self.connect_timeout = DEFAULT_CONNECT_TIMEOUT
    try:
      self.request_timeout = self.config.getint("OctoPrint", "timeout")
    except:
      self.request_timeout = DEFAULT_REQUEST_TIMEOUT
    self.url = '/'.join(["ws://{}:{}".format(host, port), 'sockjs', 'websocket'])

    self.max_reconnects = 10
    self.state = WebSocksClient.CLOSED

  def connect(self):
    logging.debug("Connecting to " + self.url)
    self.state = WebSocksClient.CONNECTING
    self._ws_connection = websocket.websocket_connect(
        self.url, callback=self._connect_callback)

  def authenticate(self, apikey):
    user = self.config.get("OctoPrint", "user")
    logging.debug("Authenticating with " + user + ":" + apikey)
    msg = '{ "auth" : "' + str(user) + ':' + str(apikey) + '" }'
    logging.info("Sending message " + msg)
    self._ws_connection.write_message(msg)

  def send(self, data):
    """
    Send message to the server
      :param str data: message.
    """
    logging.info("Sending message " + data)
    yield self._ws_connection.write_message(data)

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
    data = json.loads(msg)
    if 'connected' in data:
      logging.debug("SockJS: Socket connected")
      apik = self.config.get("OctoPrint", "apikey")
      self.authenticate(apik)
    self.parse_msg(data)

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
    logging.debug('Websocket connection error: %s', exception)

  def parse_msg(self, data):
    try:
      msg_type, payload = data.popitem()
      p = PushUpdate(msg_type, payload)
      self.config.push_updates.put(p)
    except Exception as e:
      logging.warning("Unable to parse message from Octoprint " + str(e))
      logging.warning("messsage was " + str(msg))

  def run(self):
    asyncio.set_event_loop(asyncio.new_event_loop())
    for i in range(self.request_timeout):
      if self.running:
        self.config.splash.set_status("Connecting to {} ({})".format(
            self.config.get("Server", "host"), i))
        logging.debug("Websocket connection attempt " + str(i))
        self.connect()
        ioloop.IOLoop.instance().start()
        time.sleep(1)
    self.config.splash.set_status("Unable to connect to {}".format(
        self.config.get("Server", "host")))
    self.config.splash.enable_next()

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def stop(self):
    self.running = False
    self.thread.join()


if __name__ == '__main__':

  def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M')

    settings = {'Server': {'host': 'localhost', 'port': 5000}}
    client = WebSocksClient(settings)

    def work():
      for i in range(10):
        print(i)
        time.sleep(1)

    client.start()
    threading.Thread(target=work).start()
    time.sleep(10)
    client.stop()

  main()
