import json
import tkinter as tk

import box_children
import clutter_children
import base_color_scheme
import wifi_children

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

with open("full_conf.json", "w") as fh:
  json.dump(conf, fh)
