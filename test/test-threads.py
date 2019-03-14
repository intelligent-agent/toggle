#!/usr/bin/env python2
#! -*- coding: utf-8 -*-
"""
Test threads in Clutter

Author: Elias Bakken
email: elias(at)iagent(dot)no
Website: http://www.thing-printer.com
License: GNU GPL v3: http://www.gnu.org/copyleft/gpl.html

 Redeem is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Redeem is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Toggle.  If not, see <http://www.gnu.org/licenses/>.
"""

#import subprocess
import logging
import time
import queue
import sys

from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject, GLib
from threading import Thread, current_thread
from multiprocessing import JoinableQueue
import hashlib

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')


def click(button, other=None):
  print("click func start")
  time.sleep(1)
  print("Click func end")


def thread_click(button, other):
  print("click func start")
  t = Thread(target=thread_func)
  t.start()
  t.join()
  print("Click func end")


def thread_func():
  time.sleep(1)


class Toggle:
  def __init__(self):
    Clutter.init(None)
    ui = Clutter.Script()
    ui.load_from_file("ui-threads.json")
    stage = ui.get_object("stage")
    stage.connect("destroy", self.stop)
    stage.connect("destroy", lambda w: Clutter.main_quit())

    self.loader = ui.get_object("loader")
    self.loader.set_from_file("style/loading.png")
    self.t = Clutter.PropertyTransition(property_name='rotation-angle-z')
    self.t.set_from(0)
    self.t.set_to(360)
    self.t.set_duration(3000)
    self.t.set_animatable(self.loader)
    self.t.set_repeat_count(-1)
    self.t.start()

    button1 = ui.get_object("button1")
    button1.connect("button-press-event", self.execute_in_main)
    button1.set_reactive(True)

    button2 = ui.get_object("button2")
    button2.connect("button-press-event", self.idle_add_event)
    button2.set_reactive(True)

    button3 = ui.get_object("button3")
    button3.connect("button-press-event", self.threads_idle_add_event)
    button3.set_reactive(True)

    button4 = ui.get_object("button4")
    button4.connect("button-press-event", self.execute_in_thread)
    button4.set_reactive(True)

    stage = ui.get_object("stage")
    stage.set_title("Test threads")
    stage.connect("destroy", self.stop)
    stage.show_all()

    self.events = JoinableQueue(10)

    # UI events needs to happen from within the
    # main thread. This was the only way I found that would do that.
    # It looks weirdm, but it works.
    def execute(event):
      print("Execute " + event + " from " + str(current_thread()))
      for i in range(100):
        hashlib.md5(str(list(range(100000))))
      print("Done executing")

    self.execute = execute
    stage.show()

  def execute_in_main(self, btn, other):
    self.execute("main")

  def idle_add_event(self, btn, other):
    self.events.put("glib_idle_add")

  def threads_idle_add_event(self, btn, other):
    self.events.put("threads_add_idle")

  def execute_in_thread(self, btn, other):
    self.events.put("execute_in_thread")

  def run(self):
    """ Start the process """
    self.running = True
    # Start the processes
    self.p0 = Thread(target=self.loop, args=(self.events, "Push updates"))
    self.p0.start()
    logging.info("Toggle ready")
    Clutter.main()

  def loop(self, queue, name):
    """ When a new event comes in, execute it """
    try:
      while self.running:
        try:
          event = queue.get(block=True, timeout=1)
        except queue.Empty:
          continue
        if event == "glib_idle_add":
          print("adding with Glib")
          GLib.idle_add(self.execute, event)
        elif event == "threads_add_idle":
          print("adding with Clutter")
          Clutter.threads_add_idle(0, self.execute, event)
        elif event == "execute_in_thread":
          print("Executing from thread")
          self.execute(event)

        # Must hand it over to the main thread.
        queue.task_done()
    except Exception:
      logging.exception("Exception in {} loop: ".format(name))

  def stop(self, w):
    logging.debug("Stopping Toggle")
    self.running = False
    self.p0.join()
    Clutter.main_quit()
    logging.debug("Done")


def main():
  t = Toggle()
  t.run()


if __name__ == '__main__':
  main()
