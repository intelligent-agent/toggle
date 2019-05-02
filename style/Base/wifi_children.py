import base_color_scheme

bcs = base_color_scheme.base_color_scheme

import tkinter as tk

"""
This file is part of the compositional UI config generation system

It deals with children of the wifi settings and wifi information panels.
"""



### get the screen resolution ###
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

wifi_children = [{
    "id": "wifi-text",
    "type": "ClutterText",
    "font-description": "Sans 24",
    "color": bcs["background"],
    "height": screen_height / 10.8,
    "text": "Password:",
    "x": 120,
    "y": 70
},
                 {
                     "id": "wifi-input",
                     "type": "MxEntry",
                     "password-char": 42,
                     "height": screen_height / 18,
                     "width": screen_width / 3.42,
                     "x": 120,
                     "y": 110
                 },
                 {
                     "id": "wifi-status",
                     "type": "ClutterText",
                     "font-description": "Sans 12",
                     "color": bcs["background"],
                     "x": 120,
                     "y": 200
                 }, {
                     "id": "wifi-ok",
                     "type": "MxButton",
                     "label": "OK",
                     "x": 520,
                     "y": 185
                 }, {
                     "id": "wifi-cancel",
                     "type": "MxButton",
                     "label": "Cancel",
                     "x": 586,
                     "y": 185
                 },
                 {
                     "id":
                         "keyboard",
                     "type":
                         "ClutterActor",
                     "width":
                         screen_width / 2.4,
                     "height":
                         screen_height / 4.5,
                     "y":
                         240,
                     "pivot-point-z":
                         -400.0,
                     "pivot-point": [0.5, 0.5],
                     "rotation-angle-x":
                         0.0,
                     "layout-manager": {
                         "type": "ClutterBoxLayout",
                         "orientation": 1
                     },
                     "children": [{
                         "id": "row-0",
                         "type": "ClutterActor",
                         "height": screen_height / 18,
                         "layout-manager": {
                             "type": "ClutterBoxLayout",
                             "orientation": 0,
                             "spacing": 17
                         }
                     },
                                  {
                                      "id": "row-1",
                                      "type": "ClutterActor",
                                      "height": screen_height / 18,
                                      "layout-manager": {
                                          "type": "ClutterBoxLayout",
                                          "orientation": 0,
                                          "spacing": 19
                                      }
                                  },
                                  {
                                      "id": "row-2",
                                      "type": "ClutterActor",
                                      "height": screen_height / 18,
                                      "layout-manager": {
                                          "type": "ClutterBoxLayout",
                                          "orientation": 0,
                                          "spacing": 19
                                      }
                                  },
                                  {
                                      "id": "row-3",
                                      "height": screen_height / 18,
                                      "type": "ClutterActor",
                                      "layout-manager": {
                                          "type": "ClutterBoxLayout",
                                          "orientation": 0,
                                          "spacing": 19
                                      }
                                  }]
                 }]
