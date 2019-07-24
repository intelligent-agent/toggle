#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import gi
gi.require_version('Mx', '2.0')
gi.require_version('Mash', '0.3')
gi.require_version('Cogl', '1.0')
gi.require_version('Clutter', '1.0')

from .Jog import Jog
from .Network import Network, NetworkManager, ConnMan
from .Settings import Settings
from .Splash import Splash
from .CubeTabs import CubeTabs
from .FilamentGraph import FilamentGraph
from .TemperatureGraph import TemperatureGraph
from .Graph import Graph, GraphScale, GraphPlot
from .Message import Message
from .Event import Event, PushUpdate
from .RestClient import RestClient
from .WebSocksClient import WebSocksClient
from .CascadingConfigParser import CascadingConfigParser
from .Printer import Printer
from .ModelLoader import ModelLoader
from .VolumeStage import VolumeStage
from .Plate import Plate
from .Model import Model
from .StyleLoader import StyleLoader
from threading import Thread, current_thread
from gi.repository import GObject, Clutter, Mx
from dbus.mainloop.glib import DBusGMainLoop
import os
import sys
import queue as Queue
import time
import logging

DBusGMainLoop(set_as_default=True)
"""
The main entry point for Toggle.

Author: Elias Bakken
email: elias(at)iagent(dot)no
Website: http://www.thing-printer.com
License: GNU GPL v3: http://www.gnu.org/copyleft/gpl.html

 Toggle is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Toggle is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Toggle.  If not, see <http://www.gnu.org/licenses/>.
"""

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')


class LoggerWriter:
  def __init__(self, config, logger, level):
    self.logger = logger
    self.level = level

  def write(self, message):
    if message != '\n':
      self.logger.log(self.level, message)

  def flush(self):
    pass


class Toggle:
  CONFIG_BASE = "/etc/toggle"

  def __init__(self):
    from .__init__ import __version__
    logging.info("Initializing  Toggle {}".format(__version__))

    config_files = ['default.cfg', 'printer.cfg', 'local.cfg']
    config_paths = [os.path.join(Toggle.CONFIG_BASE, f) for f in config_files]
    config = CascadingConfigParser(config_paths)

    # Get loglevel from the Config file
    level = config.getint('System', 'loglevel')
    if level > 0:
      logging.getLogger().setLevel(level)

    sys.stdout = LoggerWriter(config, logging, logging.INFO)
    sys.stderr = LoggerWriter(config, logging, logging.FATAL)

    Clutter.init(None)

    config.file_base = Toggle.CONFIG_BASE

    config.screen_width = config.getint("Screen", "width")
    config.screen_height = config.getint("Screen", "height")
    config.screen_rot = config.getint("Screen", "rotation")
    config.screen_full = config.getboolean("Screen", "fullscreen")

    config.style = StyleLoader(config)
    config.style.load_from_config()
    config.ui = config.style.ui

    config.stage = config.ui.get_object("stage")
    config.stage.connect("destroy", self.stop)
    config.stage.connect('key-press-event', self.key_press)

    config.tabs = CubeTabs(config.ui, 4)
    config.splash = Splash(config)
    config.splash.set_status("Starting Toggle {} ...".format(__version__))
    config.jog = Jog(config)
    config.temp_graph = TemperatureGraph(config)
    if config.getboolean('System', 'use-filament-graph'):
      config.filament_graph = FilamentGraph(config)
    config.network = Network.get_manager(config)
    config.settings = Settings(config)
    config.rest_client = RestClient(config)
    config.volume_stage = VolumeStage(config)
    config.message = Message(config)
    config.printer = Printer(config)
    config.loader = ModelLoader(config)
    config.plate = Plate(config)
    config.socks_client = WebSocksClient(config, self.on_connected_cb)

    # mouse
    use_mouse = int(config.get('Input', 'mouse'))
    self.cursor = config.ui.get_object("cursor")
    if use_mouse:
      config.stage.connect("motion-event", self.mouse_move)
      logging.info("Mouse is active")
    else:
      config.stage.connect("touch-event", self.mouse_move)
      logging.info("Mouse is not active, using touch instead")
      self.cursor.set_opacity(0)
    config.mouse_invert_x = config.getboolean('Input', 'mouse_invert_x')
    config.mouse_invert_y = config.getboolean('Input', 'mouse_invert_y')
    config.mouse_swap = config.getboolean('Input', 'mouse_swap_xy')

    config.push_updates = Queue.Queue(10)
    self.config = config
    config.stage.show()

  def on_connected_cb(self):
    self.config.loader.sync_and_load_models()

  def run(self):
    """
        Start the program. Can be called from
        this file or from a start-up script.
        """
    # Flip and move the stage to the right location
    # This has to be done in the application, since it is a
    # fbdev app
    #self.config.mouse_offset_x = 0
    #self.config.mouse_offset_y = 0
    if self.config.screen_rot == 90:
      self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 90.0)
      self.config.ui.get_object("all").set_position(self.config.screen_width, 0)
      #self.config.mouse_offset_x = self.config.screen_width
    elif self.config.screen_rot == 270:
      self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, -90.0)
      self.config.ui.get_object("all").set_position(0, self.config.screen_height)
    elif self.config.screen_rot == 180:
      self.config.ui.get_object("all").set_pivot_point(0.5, 0.5)
      self.config.ui.get_object("all").set_rotation_angle(Clutter.RotateAxis.Z_AXIS, 180.0)

    if self.config.screen_full:
      self.config.stage.set_fullscreen(True)
    """ Start the process """
    self.running = True
    # Start the processes
    self.p0 = Thread(target=self.loop, args=(self.config.push_updates, "Push updates"))
    self.p0.start()

    self.config.socks_client.start()
    logging.info("Toggle ready")
    Clutter.main()

  # UI events needs to happen from within the
  # main thread. This was the only way I found that would do that.
  # It looks weirdm, but it works.
  def execute(self, event):
    event.execute(self.config)
    #logging.debug("Execute from "+str(current_thread()))

  def loop(self, queue, name):
    """ When a new event comes in, execute it """
    while self.running:
      update = queue.get()
      if not update:
        continue
      # Execute any long running operations here,
      # to keep the main thread free for animations
      if update.has_thread_execution:
        update.execute_in_thread(self.config)
      # All UI updates must be handled by the main thread.
      Clutter.threads_add_idle(0, self.execute, update)

  def stop(self, w):
    logging.debug("Stopping Toggle")
    self.running = False
    self.config.push_updates.put(None)
    self.config.socks_client.stop()
    self.p0.join()
    Clutter.main_quit()
    logging.debug("Done")

  def key_press(self, actor, event):
    ''' Key press events for quick deveopment '''
    if event.unicode_value == "f":
      if self.config.stage.get_fullscreen():
        self.config.stage.set_fullscreen(False)
      else:
        self.config.stage.set_fullscreen(True)
    elif event.unicode_value == "q":
      self.stop(None)

  def mouse_move(self, actor, event):
    if hasattr(event, "x"):
      x, y = event.x, event.y
    else:
      x, y = event.get_coords()

    # Swap axes
    if self.config.mouse_swap:
      x, y = y, x
    # invert
    if self.config.mouse_invert_x:
      x = self.config.screen_height - x
    if self.config.mouse_invert_y:
      y = self.config.screen_width - y

    #logging.debug("X: {}, Y: {}".format(x, y))
    self.cursor.set_position(x, y)

    return Clutter.EVENT_PROPAGATE


def main():
  t = Toggle()
  t.run()


if __name__ == '__main__':
  main()
