#!/usr/bin/env python


from setuptools import setup, find_packages, Extension
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='Toggle',
      version='1.2.1',
      description='Embedded UI for 3D printers',
      author='Elias Bakken',
      author_email='elias@iagent.no',
      url='http://www.thing-printer.com',
      license = "CC-BY-SA-2.0",
      long_description=read('README.md'),
      packages = find_packages(),
      classifiers=[
        "Development Status :: 2 - Beta",
        "Topic :: Program",
        "License :: OSI Approved :: CC-BY-NC-2.0 License"],
      data_files=[('/etc/toggle/platforms', [
                        'models/platforms/prusa_i3.stl', 
                        'models/platforms/kossel_mini.stl', 
                        'models/platforms/makerbot_cupcake.stl']),
                  ('/usr/share/models/', [
                        'models/calibration-cube.stl', 
                        'models/treefrog.stl']),
                  ('/etc/toggle/style', [
                        'style/style.css', 
                        'style/ui_800x480.json',
			'style/ui_1920x1080.json',
                        'style/arrow_128.png',
                        'style/arrow_disabled_128.png',
                        'style/cancel_128.png',
                        'style/cancel_disabled_128.png',
                        'style/connected_128.png',
                        'style/disconnected_128.png',
                        'style/e.png',
                        'style/h.png',
                        'style/z.png', 
                        'style/heartbeat_128.png', 
                        'style/heat_128.png', 
                        'style/heated_128.png', 
                        'style/heating_128.png', 
                        'style/home.png', 
                        'style/jog_128.png', 
                        'style/loading.png', 
                        'style/pause_128.png', 
                        'style/pause_disabled_128.png', 
                        'style/play_128.png', 
                        'style/play_disabled_128.png', 
                        'style/print_128.png', 
                        'style/temperature_128.png', 
                        'style/travel_0.1_128.png', 
                        'style/travel_1_128.png', 
                        'style/travel_10_128.png', 
                        'style/travel_100_128.png', 
                        'style/Toggle_splash_900.png',
                        'style/Toggle_splash_400.png',
                        'style/pointer.png',
                        'style/fan_128.png',
                        'style/fandisable_128.png',
                        'style/motorsoff_128.png', 
                        'style/settings_128.png',
                        'style/network_128.png',
                        'style/wifi_128.png',
                        'style/slicer_128.png'
                    ]),
                  ('/etc/toggle', [
                        'configs/default.cfg', 
                        'configs/prusa_i3.cfg', 
                        'configs/kossel_mini.cfg', 
                        'configs/makerbot_cupcake.cfg', 
			'models/probe-point.stl']),
                  ('/lib/systemd/system/', [
                        'systemd/toggle.service']), 
        		  ('./', ['README.md'])],
      entry_points = {
            'console_scripts': [
                'toggle = toggle.Toggle:main'
            ]
        },
     )
