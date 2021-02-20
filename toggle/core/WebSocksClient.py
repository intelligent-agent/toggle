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


class WebSocksClient():
  """
  Base for web socket clients.
  """

  CLOSED = 0
  CONNECTING = 1
  CONNECTED = 2
  AUTHENTICATED = 3
  FAILED = 4

  def __init__(self, config, on_connected_cb):
    self.config = config
    self.on_connected_cb = on_connected_cb
    host = config.get("Server", "host")
    port = str(config.get("Server", "port"))
    self.request_timeout = self.config.getint("OctoPrint", "timeout")
    self.url = '/'.join(["ws://{}:{}".format(host, port), 'sockjs', 'websocket'])
    self.max_reconnects = 10
    self.state = WebSocksClient.CLOSED
    self._ws_connection = None
    self.ioloop = None

  def connect(self):
    logging.debug("Connecting to " + self.url)
    self.state = WebSocksClient.CONNECTING
    self._ws_connection = websocket.websocket_connect(self.url, callback=self._connect_callback)

  def send(self, data):
    """
    Send message to the server
      :param str data: message.
    """
    logging.debug("Sending message " + data)
    self._ws_connection.write_message(data)

  def close_conn(self):
    """
    Close connection.
    """
    if type(self._ws_connection) == websocket.WebSocketClientConnection:
      self._ws_connection.close()
    self.state = WebSocksClient.CLOSED

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
      self.on_connected_cb()
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
    self.ioloop.stop()
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
    host = self.config.get("Server", "host")
    for i in range(self.request_timeout):
      if self.running:
        self.config.push_updates.put(PushUpdate("set_status", f"Connecting to {host} ({i})"))
        logging.debug("Websocket connection attempt " + str(i))
        self.connect()
        self.ioloop = ioloop.IOLoop.instance()
        self.ioloop.start()
        if self.state != WebSocksClient.CLOSED:
          time.sleep(1)
    self.config.push_updates.put(PushUpdate("set_status", f"Unable to connect to {host}"))
    self.config.push_updates.put(PushUpdate("tabs_enable_next", None))

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def stop(self):
    self.running = False
    self.close_conn()
    if self.ioloop:
      self.ioloop.stop()
    self.thread.join()
