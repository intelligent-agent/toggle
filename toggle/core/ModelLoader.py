# Model loader.
# Loads the models and sets up a cycling display.

import logging
from os import listdir, remove
from os.path import isfile, join
from itertools import cycle
import re
from fnmatch import filter
import requests
from .Event import PushUpdate
from threading import Thread
import time
"""
Class that loads all models in a directory
and makes next and prev buttons change the loaded model
"""


class ModelLoader():
  def __init__(self, config):
    self.config = config
    self.model_path_base = config.get("System", "model_folder")
    self.model_selected = False
    self.models = bidirectional_cycle()

  def sync_and_load_models(self):
    self.sync_models()

  # Synchronize the files on this machine with the files from OctoPrint
  def sync_models(self):
    logging.debug("Syncing models in local folder with models in OctoPrint")
    self.remotes = self.config.rest_client.get_list_of_files()
    stls = {}
    for file in self.remotes['files']:
      if file['type'] == 'machinecode':
        model_file = ModelFile(file, self.model_path_base)
        self.models.add(model_file)
      if file['type'] == 'model':
        stls[file['hash']] = file['refs']['download']
    stl_keys = stls.keys()
    for model in self.models:
      if model.has_stl():
        hash = model.get_stl_hash()
        if hash in stl_keys:
          model.add_stl_url(stls[hash])
          model.download_stl()

  def select_model_by_filename(self, filename):
    model = self.models.select_by_name(filename)
    self.config.plate.remove_probe_points()
    self.config.printer.set_model(model.get_name())
    self.model_selected = True
    if model.has_stl():
      self.config.model.load_model(model.get_stl_path())
    else:
      self.config.model.select_missing()

  def select_none(self):
    self.config.model.hide()
    self.model_selected = False

  def select_next(self):
    self.select_by_model(self.models.next())

  def select_prev(self):
    self.select_by_model(self.models.prev())

  def select_by_model(self, model):
    logging.debug("Selecting " + model.get_name())
    p = PushUpdate("select_model", model.get_name())
    p.has_thread_execution = True
    self.config.push_updates.put(p)


class ModelFile:
  def __init__(self, model, model_path_base):
    self.model = model
    self.model_path_base = model_path_base

  def get_stl_name(self):
    return self.model['links'][0]['name']

  def has_stl(self):
    if not 'links' in self.model or len(self.model['links']) != 1:
      return False
    return self.model['links'][0]['rel'] == 'model'

  def get_stl_hash(self):
    return self.model['links'][0]['hash']

  def is_stl_available_locally(self):
    return isfile(self.get_stl_path())

  def get_stl_path(self):
    return join(self.model_path_base, self.get_stl_name())

  def get_name(self):
    return self.model['name']

  def add_stl_url(self, url):
    self.stl_url = url

  def is_local(self):
    return self.model['origin'] == 'local'

  def download_stl(self):
    url = self.stl_url
    logging.debug("downloading " + url)
    model_path = self.get_stl_path()
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


"""
Helper class for cycling through a list by
calling next and prev
"""


class bidirectional_cycle:
  def __init__(self):
    self.collection = list()
    self.index = 0
    self.has_locals = False

  def next(self):
    if not self.has_locals:
      return None
    result = self._next()
    while not result.is_local():
      result = self._next()
    return result

  def _next(self):
    self.index = (self.index + 1) % len(self.collection)
    return self.collection[self.index]

  def prev(self):
    if not self.has_locals:
      return None
    result = self._prev()
    while not result.is_local():
      result = self._prev()
    return result

  def _prev(self):
    self.index -= 1
    if self.index < 0:
      self.index = len(self.collection) - 1
    return self.collection[self.index]

  def select_by_name(self, name):
    filenames = [file_model.get_name() for file_model in self.collection]
    index = filenames.index(name)
    return self.collection[index]

  def count(self):
    return len(self.collection)

  def add(self, file):
    self.collection.append(file)
    self.has_locals |= file.is_local()

  def __iter__(self):
    return iter(self.collection)
