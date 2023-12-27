#!/usr/bin/env python3
import glob
import os
import shutil

def get_data_files():
  return [('/etc/toggle/styles/Plain', glob.glob("styles/Plain/*")),
          ('/etc/toggle/styles/Mixer', glob.glob("styles/Mixer/*")),
          ('/etc/toggle/styles/Spitzy', glob.glob("styles/Spitzy/*")),
          ('/etc/toggle/styles/Dark', glob.glob("styles/Dark/*")),
          ('/etc/toggle/styles/Black', glob.glob("styles/Black/*")),
          ('/etc/toggle', glob.glob("configs/*")),
          ('/etc/toggle/platforms', glob.glob("models/platforms/*")),
          ('/etc/toggle/models', ['models/probe-point.stl', 'models/missing-model.stl'])]

if __name__ == "__main__":
  for location, files in get_data_files():
    for file in files:
      print(location, file)
      shutil.copy(file, location)