#!/usr/bin/env python3
import os
import versioneer
from setuptools import setup, find_packages, Command


def get_data_files():
  import glob
  return [('/etc/toggle/styles/Plain', glob.glob("styles/Plain/*")),
          ('/etc/toggle/styles/Mixer', glob.glob("styles/Mixer/*")),
          ('/etc/toggle/styles/Spitzy', glob.glob("styles/Spitzy/*")),
          ('/etc/toggle/styles/Dark', glob.glob("styles/Dark/*")),
          ('/etc/toggle/styles/Black', glob.glob("styles/Black/*")),
          ('/etc/toggle', glob.glob("configs/*")),
          ('/etc/toggle/platforms', glob.glob("models/platforms/*")),
          ('/etc/toggle/models', ['models/probe-point.stl', 'models/missing-model.stl']),
          ('./', ['README.md'])]


# yapf: disable
setup(
    name='Toggle',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Embedded UI for 3D printers',
    author="Elias Bakken",
    author_email="elias@iagent.no",
    url='http://www.thing-printer.com',
    license = "CC-BY-SA-2.0",
    packages = find_packages(),
    classifiers=[
      "Development Status :: 2 - Beta",
      "Topic :: Program",
      "License :: OSI Approved :: CC-BY-NC-2.0 License"],
    platforms=["BeagleBone"],
    data_files=get_data_files(),
    # metadata for upload to PyPI
    keywords="3d printer gui",
    entry_points= {
      'console_scripts': [
        'toggle = toggle.Toggle:main',
        'toggle-update = updater:perform_update',
        'toggle-version = version:get_version'
      ]
    }
)
# yapf: enable
