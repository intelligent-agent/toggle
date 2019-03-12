# Model loader.
# Loads the models and sets up a cycling display.

import logging
from gi.repository import Clutter, Mx, Mash
from os import listdir, remove
from os.path import isfile, join
from itertools import cycle
import re
from fnmatch import filter
import requests
from .Model import Model

from .Event import PushUpdate, LocalUpdate

from threading import Thread
import time
"""
Class that loads all models in a directory
and makes next and prev buttons change the loaded model
"""


class ModelLoader(Clutter.Actor):
  def __init__(self, config):
    self.config = config
    self.path = config.get("System", "model_folder")

    self.model_selected = False

    self.model = Model(self.config)

    self.sync_models()
    self.load_models()

  def load_models(self):
    self.models = bidirectional_cycle([
        f for f in listdir(self.path) if isfile(join(self.path, f)) and (".stl" in f or ".STL" in f)
    ])

    # Load the first model
    if self.models.count() > 0:
      logging.debug("Found " + str(self.models.count()) + " models in " + self.path)
      btn_next = self.config.ui.get_object("btn-next")
      tap_next = Clutter.TapAction()
      btn_next.add_action(tap_next)
      tap_next.connect("tap", self.tap_next, None)

      btn_prev = self.config.ui.get_object("btn-prev")
      tap_prev = Clutter.TapAction()
      btn_prev.add_action(tap_prev)
      tap_prev.connect("tap", self.tap_prev, None)

      self.config.printer.set_model("")
    else:
      logging.warning("No models in " + self.path)
      self.config.printer.set_model("No models found")

  # Synchronize the files on this machine with the files from OctoPrint
  def sync_models(self):
    logging.debug("Syncing models")
    self.locals = filter(listdir(self.path), '*.[Ss][Tt][Ll]')
    self.remotes = self.config.rest_client.get_list_of_files()
    if not self.remotes:
      return
    remote_names = [f["name"] for f in self.remotes["files"] if f["type"] == "model"]

    to_delete = list(set(self.locals) - set(remote_names))
    to_download = list(set(remote_names) - set(self.locals))

    if len(to_delete):
      logging.info("Deleting {} models".format(len(to_delete)))
    if len(to_download):
      logging.info("Downloading {} models".format(len(to_download)))

    # Delete not present with OctoPrint
    for model in to_delete:
      self.delete_model(model)

    # Download missing models
    for f in self.remotes["files"]:
      if f["name"] in to_download:
        self.download_model(f)

  def download_model(self, f):
    name = f["name"]
    url = f["refs"]["download"]
    logging.debug("downloading " + url)

    model_path = join(self.path, name)
    logging.debug("saving to " + model_path)

    r = requests.get(url)
    if r.status_code == 200:
      logging.debug("Download OK")
      model = r.content
      try:
        with open(model_path, 'wb') as f:
          f.write(model)
      except IOError as e:
        logging.warning("ModelLoader: Unable to download file. Check permissions")

    else:
      logging.warning("Unable to download file. Got response: " + r.status_code)

  def delete_model(self, name):
    model_path = join(self.path, name)
    logging.warning("Syncing models with OctoPrint, deleting " + model_path)
    try:
      remove(model_path)
    except OSError as e:
      logging.error("ModelLoader: Unable to delete file. Check permissions")

  def tap_next(self, action, button, user_data):
    if not button.get_toggled():
      self.tap(self.models.next())

  def tap_prev(self, action, button, user_data):
    if not button.get_toggled():
      self.tap(self.models.prev())

  def get_model_filename(self):
    return self.models.cur()

  def tap(self, filename):
    self.model.loader.show()
    filename = re.sub(".stl", ".gco", filename, flags=re.I)
    logging.debug("Selecting " + filename)
    p = PushUpdate("select_model", filename)
    p.has_thread_execution = True
    self.config.push_updates.put(p)

  def select_model(self, filename):
    self.config.plate.remove_probe_points()
    if self.models.has(filename):
      logging.debug("showing " + filename)
      filename = self.models.select(filename)
      self.model.load_model(filename)
      self.config.printer.set_model(filename.replace(".stl", ""))
      self.model_selected = True
    else:
      self.config.printer.set_model(filename.replace(".stl", ""))
      self.model_selected = True
      self.model.select_none()
      logging.warning("Missing STL: " + filename)

  def select_none(self):
    #logging.debug("Selecting none")
    self.model.model.hide()
    self.model_selected = False


"""
Helper class for cycling through a list by
calling next and prev
"""


class bidirectional_cycle(object):
  def __init__(self, collection):
    self.collection = collection
    self.lower = [name.lower() for name in self.collection]
    self.index = 0

  def next(self):
    self.index = (self.index + 1) % len(self.collection)
    result = self.collection[self.index]
    return result

  def prev(self):
    self.index -= 1
    if self.index < 0:
      self.index = len(self.collection) - 1
    return self.collection[self.index]

  def cur(self):
    return self.collection[self.index]

  def count(self):
    return len(self.collection)

  def has(self, filename):
    return (filename.lower() in self.lower)

  def select(self, filename):
    self.index = self.lower.index(filename.lower())
    return self.collection[self.index]

  def __iter__(self):
    return self
