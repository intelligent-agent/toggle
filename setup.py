#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Toggle',
      version='0.2.0.dev1',
      description='Embedded UI for 3D printers',
      author='Elias Bakken',
      author_email='elias@iagent.no',
      url='http://www.thing-printer.com',
      license = "CC-BY-SA-2.0",
      long_description=read('README.md'),
      py_modules=['Toggle', 'Message', 'MessageListener', 'Plate', 'Model', 'VolumeStage'],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Program",
        "License :: OSI Approved :: CC-BY-NC-2.0 License",
      ],
      data_files=[('/etc/toggle/platforms', ['models/platforms/thing.ply']),
                  ('/usr/share/models/ply', ['models/treefrog.ply', 'models/suzanne.ply', 'models/teapot.ply']),
                  ('/etc/toggle/style', ['style/style.css']),
                  ('/etc/toggle', ['style/ui.json'])],
      scripts=['toggle'], 
     )

