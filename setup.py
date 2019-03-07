#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


# from toggle.__init__ import __url__
import versioneer
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
    long_description=read('README.md'),
    packages = find_packages(),
    classifiers=[
      "Development Status :: 2 - Beta",
      "Topic :: Program",
      "License :: OSI Approved :: CC-BY-NC-2.0 License"],
    platforms=["BeagleBone"],
    data_files=[
      ('/etc/toggle/platforms', [
        'models/platforms/prusa_i3.stl',
        'models/platforms/kossel_mini.stl',
        'models/platforms/makerbot_cupcake.stl']),
      ('/usr/share/models/', [
        'models/calibration-cube.stl']),
      ('/etc/toggle/style/Plain', [
        'style/Plain/style.css',
        'style/Plain/ui_800x480.json',
        'style/Plain/ui_1920x1080.json',
        'style/Plain/arrow_128.png',
        'style/Plain/arrow_disabled_128.png',
        'style/Plain/cancel_128.png',
        'style/Plain/cancel_disabled_128.png',
        'style/Plain/connected_128.png',
        'style/Plain/disconnected_128.png',
        'style/Plain/e.png',
        'style/Plain/h.png',
        'style/Plain/z.png',
        'style/Plain/heartbeat_128.png',
        'style/Plain/heater_bed_cold_128.png',
        'style/Plain/heater_bed_hot_128.png',
        'style/Plain/heater_bed_heating_128.png',
        'style/Plain/heater_cold_128.png',
        'style/Plain/heater_hot_128.png',
        'style/Plain/heater_heating_128.png',
        'style/Plain/home.png',
        'style/Plain/jog_128.png',
        'style/Plain/loading_128.png',
        'style/Plain/pause_128.png',
        'style/Plain/pause_disabled_128.png',
        'style/Plain/play_128.png',
        'style/Plain/play_disabled_128.png',
        'style/Plain/print_128.png',
        'style/Plain/temperature_128.png',
        'style/Plain/travel_0.1_128.png',
        'style/Plain/travel_1_128.png',
        'style/Plain/travel_10_128.png',
        'style/Plain/travel_100_128.png',
        'style/Plain/Toggle_splash_900.png',
        'style/Plain/Toggle_splash_400.png',
        'style/Plain/pointer.png',
        'style/Plain/fan_128.png',
        'style/Plain/fandisable_128.png',
        'style/Plain/motorsoff_128.png',
        'style/Plain/settings_128.png',
        'style/Plain/network_128.png',
        'style/Plain/wifi_128.png',
        'style/Plain/slicer_128.png'
        ]),
      ('/etc/toggle/style/Mixer', [
        'style/Mixer/style.css',
        'style/Mixer/ui_800x480.json',
        'style/Mixer/ui_1280x720.json',
        'style/Mixer/ui_1920x1080.json',
        'style/Mixer/arrow_128.png',
        'style/Mixer/arrow_disabled_128.png',
        'style/Mixer/cancel_128.png',
        'style/Mixer/cancel_disabled_128.png',
        'style/Mixer/connection_64.png',
        'style/Mixer/connection_disabled_64.png',
        'style/Mixer/e_128.png',
        'style/Mixer/h_128.png',
        'style/Mixer/z_128.png',
        'style/Mixer/heartbeat_64.png',
        'style/Mixer/heater_cold_128.png',
        'style/Mixer/heater_hot_128.png',
        'style/Mixer/heater_heating_128.png',
        'style/Mixer/heater_bed_cold_128.png',
        'style/Mixer/heater_bed_hot_128.png',
        'style/Mixer/heater_bed_heating_128.png',
        'style/Mixer/home_128.png',
        'style/Mixer/jog_128.png',
        'style/Mixer/loading_128.png',
        'style/Mixer/pause_128.png',
        'style/Mixer/pause_disabled_128.png',
        'style/Mixer/play_128.png',
        'style/Mixer/play_disabled_128.png',
        'style/Mixer/print_128.png',
        'style/Mixer/temperature_128.png',
        'style/Mixer/0.1_128.png',
        'style/Mixer/1_128.png',
        'style/Mixer/10_128.png',
        'style/Mixer/100_128.png',
        'style/Mixer/logo_600.png',
        'style/Mixer/logo_900.png',
        'style/Mixer/pointer_64.png',
        'style/Mixer/running_64.png',
        'style/Mixer/fan_on_128.png',
        'style/Mixer/fan_off_128.png',
        'style/Mixer/motor_off_128.png',
        'style/Mixer/settings_128.png',
        'style/Mixer/network_128.png',
        'style/Mixer/wifi_128.png',
        'style/Mixer/slicer_128.png'
        ]),
      ('/etc/toggle/style/Spitzy', [
        'style/Spitzy/style.css',
        #'style/Spitzy/ui_800x480.json',
        #'style/Spitzy/ui_1920x1080.json',
        #'style/Spitzy/arrow_128.png',
        #'style/Spitzy/arrow_disabled_128.png',
        #'style/Spitzy/cancel_128.png',
        #'style/Spitzy/cancel_disabled_128.png',
        #'style/Spitzy/connected_128.png',
        #'style/Spitzy/disconnected_128.png',
        #'style/Spitzy/e.png',
        #'style/Spitzy/h.png',
        #'style/Spitzy/z.png',
        #'style/Spitzy/heartbeat_128.png',
        #'style/Spitzy/heat_128.png',
        #'style/Spitzy/heated_128.png',
        #'style/Spitzy/heating_128.png',
        #'style/Spitzy/home.png',
        #'style/Spitzy/jog_128.png',
        #'style/Spitzy/loading.png',
        #'style/Spitzy/pause_128.png',
        #'style/Spitzy/pause_disabled_128.png',
        #'style/Spitzy/play_128.png',
        #'style/Spitzy/play_disabled_128.png',
        #'style/Spitzy/print_128.png',
        #'style/Spitzy/temperature_128.png',
        #'style/Spitzy/travel_0.1_128.png',
        #'style/Spitzy/travel_1_128.png',
        #'style/Spitzy/travel_10_128.png',
        #'style/Spitzy/travel_100_128.png',
        #'style/Spitzy/Toggle_splash_900.png',
        #'style/Spitzy/Toggle_splash_400.png',
        #'style/Spitzy/pointer.png',
        #'style/Spitzy/fan_128.png',
        #'style/Spitzy/fandisable_128.png',
        #'style/Spitzy/motorsoff_128.png',
        #'style/Spitzy/settings_128.png',
        #'style/Spitzy/network_128.png',
        #'style/Spitzy/wifi_128.png',
        #'style/Spitzy/slicer_128.png'
        ]),
      ('/etc/toggle', [
        'configs/default.cfg',
        'configs/prusa_i3.cfg',
        'configs/kossel_mini.cfg',
        'configs/makerbot_cupcake.cfg',
        'models/probe-point.stl']),
      ('/lib/systemd/system/', [
        'systemd/toggle.service']),
      ('./', [
        'README.md'])
    ],
    # metadata for upload to PyPI
    keywords="3d printer firmware",
    install_requires=[
      'requests',
      'pyconnman',
    ],
    #url=__url__,
    ext_modules=[
    ],
    entry_points= {
      'console_scripts': [
        'toggle = toggle.Toggle:main',
        'update-toggle = updater:perform_update',
      ]
    },
)
# yapf: enable
