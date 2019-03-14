from tornado import websocket
from tornado import gen

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


@gen.coroutine
def main():
  conn = yield websocket.websocket_connect(url)
  while True:
    msg = yield conn.read_message()
    if msg is None:
      break
    print(msg)
    # Do something with msg


main()
