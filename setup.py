#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Toggle',
      version='0.4.0.dev1',
      description='Embedded UI for 3D printers',
      author='Elias Bakken',
      author_email='elias@iagent.no',
      url='http://www.thing-printer.com',
      license = "CC-BY-SA-2.0",
      long_description=read('README.md'),
      py_modules=[
            'Toggle', 
            'Message', 
            'MessageListener', 
            'Plate', 
            'Model', 
            'VolumeStage', 
            'ModelLoader', 
            'Printer', 
            'CascadingConfigParser'],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Program",
        "License :: OSI Approved :: CC-BY-NC-2.0 License"],
      data_files=[('/etc/toggle/platforms', ['models/platforms/prusa.stl']),
                  ('/usr/share/models/', ['models/calibration-cube.stl', 'models/treefrog.stl']),
                  ('/etc/toggle/style', ['style/style.css', 'style/ui.json']),
                  ('/etc/toggle', ['configs/default.cfg'])],
      scripts=['toggle'], 
     )

