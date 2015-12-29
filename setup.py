#!/usr/bin/env python


from setuptools import setup, find_packages, Extension
import os
#from distutils.core import setup, Extension

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


#toggle_lib = Extension('toggl_lib',
#                    sources = [
#                        'toggle-lib/toggle-model.c', 
#                        'toggle-lib/toggle-box.c'])

setup(name='Toggle',
      version='0.5.0',
      description='Embedded UI for 3D printers',
      author='Elias Bakken',
      author_email='elias@iagent.no',
      url='http://www.thing-printer.com',
      license = "CC-BY-SA-2.0",
      long_description=read('README.md'),
      packages = find_packages(),
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Program",
        "License :: OSI Approved :: CC-BY-NC-2.0 License"],
      data_files=[('/etc/toggle/platforms', ['models/platforms/prusa.stl']),
                  ('/usr/share/models/', ['models/calibration-cube.stl', 'models/treefrog.stl']),
                  ('/etc/toggle/style', ['style/style.css', 'style/ui.json', 'style/button.png', 'style/button-checked.png']),
                  ('/etc/toggle', ['configs/default.cfg']),
                  ('/lib/systemd/system/', ['systemd/toggle.service', 'systemd/toggle.path']), 
        		  ('./', ['README.md'])],
      entry_points = {
            'console_scripts': [
                'toggle = toggle.Toggle:main'
            ]
        },
      #ext_modules = [toggle_lib]
     )
