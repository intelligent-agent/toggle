import json
import tkinter as tk

import box_children
import clutter_children
import base_color_scheme
import wifi_children


"""
This is the start of our compositional UI config system.

We've broken out the large JSON file into several small python files,
each of which contain dictionaries which dynamically generate UI config
JSONs, based on the current screen resolution and the base color scheme,
which can now be changed more simply.

The idea of this is that it will be run at runtime, and generate a JSON config
which is backwards-compatible at every run. Based on this, users will be able to 
change screens and other options without manually editing large and complex json files.

We've broken this compositional UI config system into several pieces:

  - base.py, the general structure and scripts to actually generate config files

  - base_color_scheme.py, which stores information about the color scheme. Users
                          who wish to change the colors should be able to edit only
                          that file, which is quite simple.

  - box_children.py, which stores information about what boxes are in the Toggle UI

  - side<N>.py where N={0,1,2,3}, stores information about each side of the box.

  - wifi_children.py, which stores information for the wifi panel of the information page.

There's more documentation about what's in each file is in that file.
"""

### finish imports ###
bc = box_children.box_children
cc = clutter_children.clutter_children
bcs = base_color_scheme.base_color_scheme
wc = wifi_children.wifi_children

### get the screen resolution ###
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

conf = [{
    "id":
        "stage",
    "type":
        "ClutterStage",
    "width":
        screen_width,
    "height":
        screen_height,
    "background-color":
        bcs["background"],
    "signals": [],
    "children": [{
        "id":
            "all",
        "type":
            "ClutterActor",
        "pivot-point": [0.0, 0.0],
        "rotation-angle-z":
            0.0,
        "children": [{
            "id": "box",
            "type": "ClutterActor",
            "width": screen_width,
            "height": screen_height,
            "pivot-point-z": -540.0,
            "pivot-point": [0.5, 0.5],
            "rotation-angle-x": 0.0,
            "layout-manager": {
                "type": "ClutterFixedLayout"
            },
            "children": bc
        },
                     {
                         "id": "state",
                         "type": "ClutterActor",
                         "width": screen_width / 3.2,
                         "height": screen_height / 16.875,
                         "x": 15,
                         "y": 1000,
                         "layout-manager": {
                             "type": "ClutterFlowLayout"
                         },
                         "children": cc
                     },
                     {
                         "id":
                             "msg",
                         "type":
                             "ClutterActor",
                         "width":
                             None,
                         "height":
                             None,
                         "background-color":
                             bcs["background"],
                         "opacity":
                             0,
                         "layout-manager": {
                             "type": "ClutterBinLayout"
                         },
                         "children": [{
                             "id": "txt",
                             "type": "ClutterText",
                             "font-description": "Sans 36",
                             "color": bcs["text_content"],
                             "height": 100
                         }]
                     },
                     {
                         "id": "wifi-overlay",
                         "type": "ClutterActor",
                         "width": None,
                         "height": None,
                         "background-color": bcs["wifi_background"],
                         "layout-manager": {
                             "type": "ClutterFixedLayout"
                         },
                         "visible": False,
                         "children": wc
                     },
                     {
                         "id":
                             "cursor",
                         "type":
                             "ClutterActor",
                         "width":
                             48,
                         "height":
                             48,
                         "children": [{
                             "id": "pointer",
                             "type": "MxButton",
                             "height": 48,
                             "width": 48,
                             "style-class": "mouse"
                         }]
                     }]
    }]
}]

with open("./style/Base/full_conf.json", "w") as fh:
  json.dump(conf, fh)
