import json
import tkinter as tk

### get the screen resolution ###
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

conf = [
  {
    "id": "stage",
    "type": "ClutterStage",
    "width": screen_width,
    "height": screen_height,
    "background-color": "base_color_scheme.background",
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
            "width": None,
            "height": None,
            "pivot-point-z": -540.0,
            "pivot-point": [
              0.5,
              0.5
            ],
            "rotation-angle-x": 0.0,
            "layout-manager": {
              "type": "ClutterFixedLayout"
            },
            "children": "box_children.json"
          },
          {
            "id": "state",
            "type": "ClutterActor",
            "width": None,
            "height": None,
            "x": 15,
            "y": 1000,
            "layout-manager": {
              "type": "ClutterFlowLayout"
            },
            "children": "clutter_children.json"
          },
          {
            "id": "msg",
            "type": "ClutterActor",
            "width": None,
            "height": None,
            "background-color": "base_color_scheme.background",
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
            "children": "wifi_children.json"
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
