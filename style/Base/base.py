import json
import tkinter as tk
import box_children.box_children as bc

### get the screen resolution ###
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

color_scheme = json.load(open("base_color_scheme.json"))["base_color_scheme"]

conf = [
  {
    "id": "stage",
    "type": "ClutterStage",
    "width": screen_width,
    "height": screen_height,
    "background-color": color_scheme,
    "signals": [],
    "children": [
      {
        "id": "all",
        "type": "ClutterActor",
        "pivot-point": [
          0.0,
          0.0
        ],
        "rotation-angle-z": 0.0,
        "children": [
          {
            "id": "box",
            "type": "ClutterActor",
            "width": screen_width,
            "height": screen_height,
            "pivot-point-z": -540.0,
            "pivot-point": [
              0.5,
              0.5
            ],
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
            "children": json.load(open("clutter_children.py"))["clutter_children"]
          },
          {
            "id": "msg",
            "type": "ClutterActor",
            "width": None,
            "height": None,
            "background-color": color_scheme["background"],
            "opacity": 0,
            "layout-manager": {
              "type": "ClutterBinLayout"
            },
            "children": [
              {
                "id": "txt",
                "type": "ClutterText",
                "font-description": "Sans 36",
                "color": "base_color_scheme.text_content",
                "height": 100
              }
            ]
          },
          {
            "id": "wifi-overlay",
            "type": "ClutterActor",
            "width": None,
            "height": None,
            "background-color": "base_color_scheme.wifi_background",
            "layout-manager": {
              "type": "ClutterFixedLayout"
            },
            "visible": False,
            "children": "wifi_children.py"
          },
          {
            "id": "cursor",
            "type": "ClutterActor",
            "width": 48,
            "height": 48,
            "children": [
              {
                "id": "pointer",
                "type": "MxButton",
                "height": 48,
                "width": 48,
                "style-class": "mouse"
              }
            ]
          }
        ]
      }
    ]
  }
]


with open("full_conf.json") as fh:
  json.dump(conf, fh)
